// CUC-Array v1: 5-Pair 40kHz Ultrasonic Levitator C-Bracket (dimensions in mm)
gap_height    = 34.3;  // 4-wavelength resonant cavity (4 * 8.575 mm)
transducer_d  = 16.2;  // 16.0 mm TCT40-16T + 0.2 mm clearance
pitch_x       = 17.0;  // Center-to-center emitter spacing
num_nodes     = 5;     // 5 top + 5 bottom emitters
bar_thickness = 10.0;
bar_depth     = 24.0;
spine_width   = 18.0;

array_span = (num_nodes - 1) * pitch_x;
arm_length = spine_width + array_span + 26.0;
total_h    = gap_height + 2 * bar_thickness;

difference() {
    union() {
        cube([arm_length + 10, bar_depth, bar_thickness]); // Bottom arm + foot
        cube([spine_width, bar_depth, total_h]);          // Vertical spine
        translate([0, 0, total_h - bar_thickness])
            cube([arm_length, bar_depth, bar_thickness]); // Top arm
    }
    for (i = [0 : num_nodes - 1]) {
        x_pos = spine_width + 13.0 + i * pitch_x;
        translate([x_pos, bar_depth / 2, -1])
            cylinder(h = total_h + 2, d = transducer_d, $fn = 60);
    }
}
