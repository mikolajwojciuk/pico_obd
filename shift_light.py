from machine import Pin, Timer
import neopixel


class SHIFT_LIGHT:
    def __init__(
        self,
        pixel_count: int,
        segments_count: int,
        pin: int,
        base_colour: tuple[int, int, int],
        limiter_colour: tuple[int, int, int],
        minimum_rpm: int,
        maximum_rpm: int,
    ):
        self.n_pixels: int = pixel_count
        self.n_segments: int = segments_count
        self.pin: int = pin
        self.shift_light = neopixel.NeoPixel(Pin(self.pin), self.n_pixels)
        self.led_segments_list: list[list[int]] = self.split_led_into_segments(
            self.n_pixels, self.n_segments
        )
        self.rpm_segments_list: list[int] = self.split_rpm_into_segments(
            minimum_rpm, maximum_rpm, self.n_segments + 1
        )
        self.base_colour: tuple = base_colour
        self.limiter_colour: tuple = limiter_colour
        self.min_rpm: int = minimum_rpm
        self.max_rpm: int = maximum_rpm
        self.limiter_counter = 0
        self.limiter_status = False
        self.limiter_counter_toggle = 1

    def split_led_into_segments(
        self, n_pixels: int, n_segments: int
    ) -> list[list[int]]:
        k, m = divmod(len(range(n_pixels)), n_segments)
        segments = list(
            list(range(n_pixels))[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)]
            for i in range(n_segments)
        )
        return segments

    def split_rpm_into_segments(
        self, min_rpm: int, max_rpm: int, n_segments: int = 5
    ) -> list[int]:
        rpm_diff = (max_rpm - min_rpm) / n_segments
        rpm_segments = [int(min_rpm + n * rpm_diff) for n in range(n_segments + 1)]
        return rpm_segments

    def rpm_segment(self, rpm) -> int:
        segment = list(map(lambda i: i > rpm, self.rpm_segments_list)).index(True)
        return segment

    def display_rpm(self, rpm: int) -> None:
        # Function for turning on LEDs according to rpm
        if rpm >= self.max_rpm:
            rpm = self.max_rpm - 1
        for led_index in range(self.n_pixels):
            self.shift_light[led_index] = (0, 0, 0)

        segments_count = self.rpm_segment(rpm)

        if segments_count == 0:
            for n in range(self.n_pixels):
                self.shift_light[n] = (0, 0, 0)
            self.shift_light.write()

        elif segments_count <= self.n_segments:
            led_indexes = [
                item
                for sublist in self.led_segments_list[:segments_count]
                for item in sublist
            ]
            for led_index in led_indexes:
                self.shift_light[led_index] = self.base_colour
            self.shift_light.write()
        elif segments_count == self.n_segments + 1:
            self.limiter_counter += 1
            self.toggle_limiter()
            if self.limiter_status:
                for led_index in range(self.n_pixels):
                    self.shift_light[led_index] = self.limiter_colour
                self.shift_light.write()
            if not self.limiter_status:
                for led_index in range(self.n_pixels):
                    self.shift_light[led_index] = (0, 0, 0)
                self.shift_light.write()

    def toggle_limiter(self):
        if self.limiter_counter >= self.limiter_counter_toggle:
            self.limiter_counter = 0
            self.limiter_status = not self.limiter_status
