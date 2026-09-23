import numpy as np
from pydub import AudioSegment
from PIL import ImageDraw
import config

class AudioSpectrumVisualizer:
    def __init__(self, audio_path: str, fps: int = 30):
        self.fps = fps
        self.audio_path = audio_path
        self.num_bars = config.VIS_NUM_BARS
        self.min_height = config.VIS_MIN_HEIGHT
        self.max_height = config.VIS_MAX_HEIGHT
        self.center_x = config.VIS_CENTER_X
        self.base_y = config.VIS_BASE_Y
        self.bar_width = config.VIS_BAR_WIDTH
        self.bar_spacing = config.VIS_BAR_SPACING
        self.color = config.VIS_COLOR

        self._precompute_spectrum()

    def _precompute_spectrum(self):
        """
        Precomputes bar heights for every frame across the entire audio timeline.
        """
        seg = AudioSegment.from_file(self.audio_path)
        samples = np.array(seg.get_array_of_samples(), dtype=np.float32)
        if seg.channels == 2:
            samples = samples.reshape((-1, 2)).mean(axis=1)

        sr = seg.frame_rate
        total_duration = len(samples) / float(sr)
        self.total_frames = int(np.ceil(total_duration * self.fps))

        win_size = 2048
        half_win = win_size // 2
        hanning = np.hanning(win_size)

        # Voice frequency range: 100 Hz to 4500 Hz
        freqs = np.fft.rfftfreq(win_size, 1.0 / sr)
        valid_indices = np.where((freqs >= 100) & (freqs <= 4500))[0]
        
        # Divide into num_bars logarithmic bands
        band_edges = np.logspace(np.log10(valid_indices[0]), np.log10(valid_indices[-1]), self.num_bars + 1).astype(int)

        raw_frames = np.zeros((self.total_frames, self.num_bars), dtype=np.float32)

        for frame_idx in range(self.total_frames):
            center_sample = int(frame_idx * (sr / self.fps))
            start_sample = max(0, center_sample - half_win)
            end_sample = min(len(samples), start_sample + win_size)

            chunk = samples[start_sample:end_sample]
            if len(chunk) < win_size:
                chunk = np.pad(chunk, (0, win_size - len(chunk)))

            fft_vals = np.abs(np.fft.rfft(chunk * hanning))

            for b in range(self.num_bars):
                low_idx = band_edges[b]
                high_idx = max(low_idx + 1, band_edges[b + 1])
                val = np.mean(fft_vals[low_idx:high_idx])
                raw_frames[frame_idx, b] = val

        # Normalize and apply temporal smoothing
        # Normalize relative to overall 95th percentile
        p95 = np.percentile(raw_frames, 95)
        if p95 > 0:
            norm_frames = raw_frames / p95
        else:
            norm_frames = raw_frames

        norm_frames = np.clip(norm_frames, 0.0, 1.8)

        # Smooth using attack/decay filter
        smoothed = np.zeros_like(norm_frames)
        prev_vals = np.zeros(self.num_bars, dtype=np.float32)

        for f in range(self.total_frames):
            curr = norm_frames[f]
            # Higher center weighting so center bars are slightly taller
            center_weight = 0.7 + 0.45 * np.sin(np.linspace(0, np.pi, self.num_bars))
            curr = curr * center_weight

            # Attack / decay
            for b in range(self.num_bars):
                if curr[b] > prev_vals[b]:
                    prev_vals[b] = prev_vals[b] * 0.3 + curr[b] * 0.7  # Fast attack
                else:
                    prev_vals[b] = prev_vals[b] * 0.75 + curr[b] * 0.25 # Smooth decay
            smoothed[f] = prev_vals

        # Map to pixel heights (min_height to max_height)
        self.heights = self.min_height + (smoothed * (self.max_height - self.min_height)).astype(int)
        self.heights = np.clip(self.heights, self.min_height, self.max_height)

    def draw_frame(self, draw: ImageDraw.ImageDraw, frame_idx: int):
        """
        Renders the animated visualizer bars for the given frame_idx onto the PIL ImageDraw context.
        """
        if frame_idx >= len(self.heights):
            h_row = np.full(self.num_bars, self.min_height)
        else:
            h_row = self.heights[frame_idx]

        total_width = (self.num_bars - 1) * self.bar_spacing + self.bar_width
        start_x = self.center_x - (total_width // 2)

        for i in range(self.num_bars):
            h = int(h_row[i])
            bx = start_x + (i * self.bar_spacing)
            half_h = max(2, h // 2)
            top_y = self.base_y - half_h
            bot_y = self.base_y + half_h

            # Draw rounded bar / pill
            draw.rounded_rectangle(
                [bx, top_y, bx + self.bar_width, bot_y],
                radius=self.bar_width // 2,
                fill=self.color
            )
