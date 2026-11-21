#include <Arduino.h>
#include <math.h>

const int PIN_TOP_A   = 4;
const int PIN_TOP_B   = 5;
const int PIN_BOT_A   = 6;
const int PIN_BOT_B   = 7;

const int PIN_MIC_ADC = 1;
const int PIN_POT_ADC = 2;
const int PIN_POT_EN  = 3;

const uint32_t CARRIER_FREQ_HZ = 40000;
const uint8_t  PWM_RES_BITS    = 10;
const uint32_t PWM_MAX_TICKS   = (1 << PWM_RES_BITS) - 1;
const uint32_t HALF_PERIOD     = 512;

const float ALPHA = 1.0f;
const float BETA  = 0.8f;
const float GAMMA = 0.7f;

const float K_RESTORE_MAX = 0.85f;
const float STEP_DEG      = 15.0f;

float baseline_mic_rms       = 50.0f;
float baseline_cascade_index = 1.0f;
float dynamic_d_threshold    = 0.35f;
float dynamic_cascade_warn   = 1.80f;
float dynamic_cascade_trip   = 3.00f;

float target_phase_deg   = 0.0f;
float actual_phase_deg   = 0.0f;
float k_restore_active   = 0.0f;
int   cascade_gate_state = 0;

void setArrayPhaseShift(float degrees) {
  while (degrees < 0.0f) degrees += 360.0f;
  while (degrees >= 360.0f) degrees -= 360.0f;

  uint32_t shift_ticks = (uint32_t)((degrees / 360.0f) * PWM_MAX_TICKS);

  ledcWritePhase(PIN_TOP_A, 0);
  ledcWritePhase(PIN_TOP_B, HALF_PERIOD);

  ledcWritePhase(PIN_BOT_A, shift_ticks % PWM_MAX_TICKS);
  ledcWritePhase(PIN_BOT_B, (shift_ticks + HALF_PERIOD) % PWM_MAX_TICKS);
}

void measureAcousticField(float &rms_out, float &jitter_out, float &raw_cascade_out) {
  const int SAMPLES = 128;
  float readings[128];
  float sum = 0.0f;

  for (int i = 0; i < SAMPLES; i++) {
    readings[i] = (float)analogRead(PIN_MIC_ADC);
    sum += readings[i];
    delayMicroseconds(15);
  }

  float mean = sum / SAMPLES;
  float sq_sum = 0.0f;
  float diff_sq_sum = 0.0f;

  for (int i = 0; i < SAMPLES; i++) {
    float centered = readings[i] - mean;
    sq_sum += centered * centered;
    if (i > 0) {
      float step_diff = readings[i] - readings[i - 1];
      diff_sq_sum += step_diff * step_diff;
    }
  }

  float coherent_energy = (sq_sum / SAMPLES) + 1.0f;
  float enstrophy_proxy = diff_sq_sum / (SAMPLES - 1);

  rms_out = sqrtf(sq_sum / SAMPLES);
  jitter_out = sqrtf(enstrophy_proxy) / (rms_out + 1.0f);
  raw_cascade_out = enstrophy_proxy / coherent_energy;
}

void runAutoCalibration() {
  Serial.println("# [CALIBRATING] Hold cavity steady for 2 seconds...");
  target_phase_deg = 0.0f;
  actual_phase_deg = 0.0f;
  setArrayPhaseShift(0.0f);
  delay(300);

  const int CAL_WINDOWS = 100;
  float sum_rms = 0.0f;
  float sum_jitter = 0.0f;
  float sum_cascade = 0.0f;
  float sq_sum_cascade = 0.0f;

  for (int w = 0; w < CAL_WINDOWS; w++) {
    float r_s = 0.0f, j_s = 0.0f, c_s = 0.0f;
    measureAcousticField(r_s, j_s, c_s);
    sum_rms += r_s;
    sum_jitter += j_s;
    sum_cascade += c_s;
    sq_sum_cascade += c_s * c_s;
    delay(15);
  }

  baseline_mic_rms       = max(sum_rms / CAL_WINDOWS, 50.0f);
  float mean_jitter      = sum_jitter / CAL_WINDOWS;
  baseline_cascade_index = max(sum_cascade / CAL_WINDOWS, 1e-4f);

  float var_cascade = max(0.0f, (sq_sum_cascade / CAL_WINDOWS) - (baseline_cascade_index * baseline_cascade_index));
  float std_cascade_norm = sqrtf(var_cascade) / baseline_cascade_index;

  float d_quiet = BETA * constrain(mean_jitter * 1.5f, 0.0f, 2.0f);
  dynamic_d_threshold  = constrain(max(0.18f, 3.5f * d_quiet), 0.18f, 0.65f);
  dynamic_cascade_warn = constrain(1.5f + 3.0f * std_cascade_norm, 1.5f, 2.5f);
  dynamic_cascade_trip = constrain(2.5f + 5.0f * std_cascade_norm, 2.5f, 4.5f);

  Serial.print("# [CALIBRATED] RMS_base=");
  Serial.print(baseline_mic_rms, 1);
  Serial.print(" | D_quiet=");
  Serial.print(d_quiet, 3);
  Serial.print(" | D_thresh=");
  Serial.print(dynamic_d_threshold, 3);
  Serial.print(" | Cascade_Warn/Trip=");
  Serial.print(dynamic_cascade_warn, 2);
  Serial.print("/");
  Serial.println(dynamic_cascade_trip, 2);
}

void updateManualTarget() {
  if (digitalRead(PIN_POT_EN) == HIGH) {
    int raw_pot = analogRead(PIN_POT_ADC);
    target_phase_deg = ((float)raw_pot / 4095.0f) * 360.0f - 180.0f;
  }

  while (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == '+' || cmd == '=') {
      target_phase_deg += STEP_DEG;
    } else if (cmd == '-' || cmd == '_') {
      target_phase_deg -= STEP_DEG;
    } else if (cmd == 'r' || cmd == 'R' || cmd == '0') {
      target_phase_deg = 0.0f;
    } else if (cmd == 't' || cmd == 'T') {
      target_phase_deg = Serial.parseFloat();
    } else if (cmd == 'c' || cmd == 'C') {
      runAutoCalibration();
    }
  }

  float max_slew = (cascade_gate_state >= 1) ? 1.5f : 4.0f;
  float delta = target_phase_deg - actual_phase_deg;
  actual_phase_deg += constrain(delta, -max_slew, max_slew);
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  analogReadResolution(12);
  pinMode(PIN_POT_EN, INPUT_PULLDOWN);

  ledcAttach(PIN_TOP_A, CARRIER_FREQ_HZ, PWM_RES_BITS);
  ledcAttach(PIN_TOP_B, CARRIER_FREQ_HZ, PWM_RES_BITS);
  ledcAttach(PIN_BOT_A, CARRIER_FREQ_HZ, PWM_RES_BITS);
  ledcAttach(PIN_BOT_B, CARRIER_FREQ_HZ, PWM_RES_BITS);

  ledcWrite(PIN_TOP_A, HALF_PERIOD);
  ledcWrite(PIN_TOP_B, HALF_PERIOD);
  ledcWrite(PIN_BOT_A, HALF_PERIOD);
  ledcWrite(PIN_BOT_B, HALF_PERIOD);

  Serial.println("==============================================================================================");
  Serial.println("CUC-Array v1 Auto-Calibrated | Keys: '+' right, '-' left, 'r' reset, 'c' re-calibrate");
  runAutoCalibration();
  Serial.println("Time_ms, Target_deg, r_coh, N_noise, FC_drift, D_load, S_persist, Cascade_Gamma, Gate_State, k_restore");
}

void loop() {
  updateManualTarget();

  float current_rms = 0.0f;
  float raw_jitter  = 0.0f;
  float raw_cascade = 0.0f;
  measureAcousticField(current_rms, raw_jitter, raw_cascade);

  float ratio = current_rms / baseline_mic_rms;
  float r = constrain(1.0f - fabsf(1.0f - ratio), 0.0f, 1.0f);
  float N = constrain(raw_jitter * 1.5f, 0.0f, 2.0f);

  float phase_error_rad = (actual_phase_deg - target_phase_deg) * (PI / 180.0f);
  float FC = powf(sinf(phase_error_rad * 0.5f), 2.0f);

  float cascade_gamma = raw_cascade / baseline_cascade_index;

  float D = ALPHA * (1.0f - r) + BETA * N + GAMMA * FC;
  float S = r * expf(-D);

  if (D > dynamic_d_threshold || cascade_gamma >= dynamic_cascade_trip) {
    cascade_gate_state = 2;
  } else if (cascade_gamma >= dynamic_cascade_warn) {
    cascade_gate_state = 1;
  } else {
    cascade_gate_state = 0;
  }

  if (cascade_gate_state == 2) {
    float excess_d = max(0.0f, D - dynamic_d_threshold);
    float excess_g = max(0.0f, (cascade_gamma - dynamic_cascade_trip) * 0.15f);
    k_restore_active = constrain((excess_d + excess_g) * 1.5f, 0.25f, K_RESTORE_MAX);
    actual_phase_deg -= k_restore_active * sinf(phase_error_rad) * 15.0f;
  } else {
    k_restore_active = 0.0f;
  }

  setArrayPhaseShift(actual_phase_deg);

  Serial.print(millis());             Serial.print(", ");
  Serial.print(target_phase_deg, 1);  Serial.print(", ");
  Serial.print(r, 3);                 Serial.print(", ");
  Serial.print(N, 3);                 Serial.print(", ");
  Serial.print(FC, 3);                Serial.print(", ");
  Serial.print(D, 3);                 Serial.print(", ");
  Serial.print(S, 3);                 Serial.print(", ");
  Serial.print(cascade_gamma, 2);     Serial.print(", ");
  Serial.print(cascade_gate_state);   Serial.print(", ");
  Serial.println(k_restore_active, 3);

  delay(10);
}
