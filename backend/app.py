import os
import replicate
import requests
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from PIL import Image
import io
import time

load_dotenv()
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
rep_client = replicate.Client(api_token=REPLICATE_API_TOKEN)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("backend/generated", exist_ok=True)

@app.post("/generate_sprite/")
async def generate_sprite(prompt: str = Form(...), num_frames: int = Form(4)):
    try:
        output_urls = rep_client.run(
            "fofr/pixel-art-xl",
            input={
                "prompt": f"{prompt}, pixel art, 32x32 pixels, transparent background",
                "num_outputs": num_frames
            }
        )
        frames = []
        for url in output_urls:
            img_data = requests.get(url).content
            img = Image.open(io.BytesIO(img_data)).convert("RGBA").resize((32, 32))
            frames.append(img)

        timestamp = int(time.time())
        # 스프라이트 시트 저장
        sheet_width = 32 * len(frames)
        sprite_sheet = Image.new("RGBA", (sheet_width, 32))
        for i, frame in enumerate(frames):
            sprite_sheet.paste(frame, (i * 32, 0))
        sheet_path = f"backend/generated/sprite_sheet_{timestamp}.png"
        sprite_sheet.save(sheet_path)

        # GIF 애니메이션 저장
        gif_path = f"backend/generated/sprite_anim_{timestamp}.gif"
        frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=150, loop=0)

        return {
            "frames": output_urls,
            "sprite_sheet": f"/backend/generated/sprite_sheet_{timestamp}.png",
            "gif": f"/backend/generated/sprite_anim_{timestamp}.gif"
        }
    except Exception as e:
        return {"error": str(e)}