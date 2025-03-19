document.getElementById("generateForm").onsubmit = async function(e) {
  e.preventDefault();
  const formData = new FormData(this);
  const response = await fetch("http://127.0.0.1:8000/generate_sprite/", {
    method: "POST",
    body: new URLSearchParams(formData)
  });
  const data = await response.json();
  const gallery = document.getElementById("gallery");
  gallery.innerHTML = "";
  if (data.frames) {
    data.frames.forEach(url => {
      const img = document.createElement("img");
      img.src = url;
      img.width = 64;
      img.height = 64;
      img.className = "border rounded";
      gallery.appendChild(img);
    });
    const sheet = document.createElement("img");
    sheet.src = data.sprite_sheet;
    sheet.className = "border rounded";
    const gif = document.createElement("img");
    gif.src = data.gif;
    gif.className = "border rounded";
    gallery.appendChild(sheet);
    gallery.appendChild(gif);
    const dl = document.createElement("a");
    dl.href = data.gif;
    dl.download = "sprite.gif";
    dl.innerText = "GIF 다운로드";
    dl.className = "block text-blue-600 underline";
    gallery.appendChild(dl);
  } else {
    gallery.innerText = "에러 발생: " + data.error;
  }
};