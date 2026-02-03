#include QMK_KEYBOARD_H
#include "via.h"
#include "raw_hid.h"
#include "print.h"
#include "qp.h"
#include "font/proton_mono20.qff.h"

// you might have to rearrange these based on your layer order:
enum layer_names { _LAYER0, _LAYER1, _LAYER2, _LAYER3, _LAYER4 };

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    /* LAYER 0 */
    [0] = LAYOUT(TO(1), TO(1), TO(1), TO(1), TO(1), TO(1), TO(1), TO(1), TO(1), TO(1), TO(1), TO(1), TO(1), TO(1), TO(1), TO(1)),

    /* LAYER 1 */
    [1] = LAYOUT(TO(2), TO(2), TO(2), TO(2), TO(2), TO(2), TO(2), TO(2), TO(2), TO(2), TO(2), TO(2), TO(2), TO(2), TO(2), TO(2)),

    /* LAYER 2 */
    [2] = LAYOUT(TO(3), TO(3), TO(3), TO(3), TO(3), TO(3), TO(3), TO(3), TO(3), TO(3), TO(3), TO(3), TO(3), TO(3), TO(3), TO(3)),

    /* LAYER 3 */
    [3] = LAYOUT(TO(4), TO(4), TO(4), TO(4), TO(4), TO(4), TO(4), TO(4), TO(4), TO(4), TO(4), TO(4), TO(4), TO(4), TO(4), TO(4)),

    /* LAYER 4 */
    [4] = LAYOUT(TO(0), TO(0), TO(0), TO(0), TO(0), TO(0), TO(0), TO(0), TO(0), TO(0), TO(0), TO(0), TO(0), TO(0), TO(0), TO(0))};

#if defined(ENCODER_MAP_ENABLE)
const uint16_t PROGMEM encoder_map[][NUM_ENCODERS][NUM_DIRECTIONS] = {
    [0] = {ENCODER_CCW_CW(KC_VOLD, KC_VOLU)}, [1] = {ENCODER_CCW_CW(UG_SATD, UG_SATU)}, [2] = {ENCODER_CCW_CW(UG_SPDD, UG_SPDU)}, [3] = {ENCODER_CCW_CW(KC_RIGHT, KC_LEFT)}, [4] = {ENCODER_CCW_CW(KC_RIGHT, KC_LEFT)},
};
#endif

painter_device_t      display;
painter_font_handle_t my_font;
uint32_t              oled_timer          = 0;
uint8_t               oled_timeout_config = 1; // 0=10s, 1=30s, 2=60s, 3=Never
bool                  oled_is_on          = true;

void render_oled_page_layer_badge(layer_state_t state);

void keyboard_post_init_user(void) {
    // Initialize the display
    display = qp_sh1106_make_i2c_device(128, 32, 0x3C);
    qp_init(display, QP_ROTATION_0);

    // Turn on the LCD and clear the display
    qp_power(display, true);
    qp_clear(display);

    my_font = qp_load_font_mem(font_proton_mono20);
    render_oled_page_layer_badge(layer_state);

    oled_timer = timer_read32();
}

bool process_record_user(uint16_t keycode, keyrecord_t *record) {
    // Send key event to host via Raw HID
    // Protocol: [0xFB, 0x02, row, col, pressed]
    uint8_t data[32];
    memset(data, 0, 32);
    data[0] = 0xFB; // Event Packet
    data[1] = 0x02; // Key Event
    data[2] = record->event.key.row;
    data[3] = record->event.key.col;
    data[4] = record->event.pressed ? 1 : 0;
    raw_hid_send(data, 32);

    if (record->event.pressed) {
        oled_timer = timer_read32();
        if (!oled_is_on) {
            qp_power(display, true);
            oled_is_on = true;
            // Refresh display when turning back on
            render_oled_page_layer_badge(layer_state);
        }
    }
    return true;
}

void housekeeping_task_user(void) {
    if (oled_is_on && oled_timeout_config != 3) {
        uint32_t timeout_ms = 30000;
        switch (oled_timeout_config) {
            case 0:
                timeout_ms = 10000;
                break;
            case 1:
                timeout_ms = 30000;
                break;
            case 2:
                timeout_ms = 60000;
                break;
            default:
                timeout_ms = 30000;
                break;
        }

        if (timer_elapsed32(oled_timer) > timeout_ms) {
            qp_power(display, false);
            oled_is_on = false;
        }
    }
}

void render_oled_page_layer_badge(layer_state_t state) {
    uint8_t layer          = get_highest_layer(state);
    char    layer_text[10] = {0};

    qp_clear(display);

    // Create layer text: "LAYER 0" through "LAYER 4"
    sprintf(layer_text, "LAYER %d", layer);

    // Calculate text width to center it
    int text_width = qp_textwidth(my_font, layer_text);
    int x_pos      = (128 - text_width) / 2;
    int y_pos      = 3;

    // Draw the layer text
    qp_drawtext(display, x_pos, y_pos, my_font, layer_text);

    qp_flush(display);
}

layer_state_t layer_state_set_user(layer_state_t state) {
    render_oled_page_layer_badge(state);

    // Send layer change to host
    uint8_t layer = get_highest_layer(state);
    uint8_t data[32];
    memset(data, 0, 32);
    data[0] = 0xFB; // Event Packet
    data[1] = 0x01; // Layer Change
    data[2] = layer;
    raw_hid_send(data, 32);

    return state;
}

// Raw HID handler for auto-layer switching
void raw_hid_receive_kb(uint8_t *data, uint8_t length) {
    if (data[0] == 0xFC) {
        switch (data[1]) {
            case 0x01: // Switch to layer
                layer_move(data[2]);
                data[1] = 0xFD; // Acknowledge
                break;
            case 0x02: // Get current layer
                data[2] = get_highest_layer(layer_state);
                data[1] = 0xFD; // Acknowledge
                break;
            case 0x03: // Set OLED Timeout
                oled_timeout_config = data[2];
                oled_timer          = timer_read32(); // Reset timer
                if (!oled_is_on) {
                    qp_power(display, true);
                    oled_is_on = true;
                }
                data[1] = 0xFD; // Acknowledge
                break;
            case 0x04: // Get OLED Timeout
                data[2] = oled_timeout_config;
                data[1] = 0xFD; // Acknowledge
                break;
        }
    }
    raw_hid_send(data, length);
}

// RGB LED configuration
#ifdef RGB_MATRIX_ENABLE
led_config_t g_led_config = {{// Key Matrix to LED Index
                              {NO_LED},
                              {0, 1, 2, 3},
                              {7, 6, 5, 4},
                              {8, 9, 10, 11}},
                             {// Row 1 LEDs (0-3)
                              {0, 21},
                              {75, 21},
                              {149, 21},
                              {224, 21},
                              // Row 2 LEDs (4-7)
                              {0, 42},
                              {75, 42},
                              {149, 42},
                              {224, 42},
                              // Row 3 LEDs (8-11)
                              {0, 63},
                              {75, 63},
                              {149, 63},
                              {224, 63}},
                             {
                                 // LED Index to Flag
                                 4, 4, 4, 4, // Row 1 LEDs - key lights
                                 4, 4, 4, 4, // Row 2 LEDs - key lights
                                 4, 4, 4, 4  // Row 3 LEDs - key lights
                             }};
#endif
