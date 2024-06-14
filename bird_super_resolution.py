import torchvision.transforms.functional as F
from comfy.utils import ProgressBar
from .birdlib.api import BIRD

class BirdSuperResolution:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL", {"forceInput": True}),
                "image": ("IMAGE", {"forceInput": True}),

                "optimization_steps": ("INT", {"default": 100}),
                "lr": ("FLOAT", {"default": 0.001, "step": 0.001}),
                "delta_t": ("INT", {"default": 100}),
                "downsampling_ratio": ("INT", {"default": 8}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffff}),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ()

    FUNCTION = "execute"

    CATEGORY = "NuA/BIRD"

    def execute(self, model, image, optimization_steps, lr, delta_t, downsampling_ratio, seed):
        bird = BIRD(model)

        task = "super_resolution"
        task_config = {
            "Optimization_steps": optimization_steps,
            "lr": lr,
            "delta_t": delta_t,
            "downsampling_ratio": downsampling_ratio,
            "seed": seed,
        }

        img = image.squeeze(0)
        img = img.permute(2, 0, 1)
        img = F.to_pil_image(img)

        img = bird.process(
            task,
            task_config,
            img,
        )

        img = F.to_tensor(img)
        img = img.permute(1, 2, 0).unsqueeze(0)

        return (img)
