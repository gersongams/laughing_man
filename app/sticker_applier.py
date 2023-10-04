import cv2


class StickerApplier:
    def __init__(self, sticker_path):
        self.sticker = cv2.imread(sticker_path, cv2.IMREAD_UNCHANGED)
        if self.sticker is None:
            raise FileNotFoundError("Sticker not found or failed to load.")

    def apply_sticker(self, frame, faces):
        for box in faces:
            (startX, startY, endX, endY) = box
            w = endX - startX
            h = endY - startY
            resized_sticker = cv2.resize(self.sticker, (w, h))

            # Debugging: print shapes
            # print(f"Target shape: {frame[startY:endY, startX:endX].shape}, Resized sticker shape: {resized_sticker.shape}")

            # Separate the BGR and alpha channels (if present)
            if resized_sticker.shape[2] == 4:
                bgr = resized_sticker[:, :, :3]
                alpha = resized_sticker[:, :, 3]
            else:
                bgr = resized_sticker
                alpha = None

            # Apply the sticker to the frame
            for c in range(0, 3):
                if alpha is not None:
                    alpha_multiplier = 1 - alpha / 255.0
                    bgr_new = bgr[:, :, c] * (alpha / 255.0)
                    frame[startY:endY, startX:endX, c] = frame[startY:endY, startX:endX, c] * alpha_multiplier + bgr_new
                else:
                    frame[startY:endY, startX:endX, c] = bgr[:, :, c]
