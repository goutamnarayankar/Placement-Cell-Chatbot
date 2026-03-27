// chat.js - controls chat UI and resume upload interaction
document.addEventListener("DOMContentLoaded", function(){

  const chatWindow = document.getElementById("chat-window");
  const chatForm = document.getElementById("chat-form");
  const chatInput = document.getElementById("chat-input");

  const uploadBtn = document.getElementById("upload-btn");
  const resumeFile = document.getElementById("resume-file");
  const dropzone = document.querySelector(".dropzone");


  /* -------------------------------
     DRAG & DROP RESUME HANDLER
  ------------------------------- */

  if(dropzone){
    dropzone.addEventListener("click", ()=> resumeFile.click());

    dropzone.addEventListener("dragover", e => { 
      e.preventDefault(); 
      dropzone.classList.add("drag"); 
    });

    dropzone.addEventListener("dragleave", ()=> { 
      dropzone.classList.remove("drag"); 
    });

    dropzone.addEventListener("drop", e => {
      e.preventDefault();
      dropzone.classList.remove("drag");
      const f = e.dataTransfer.files[0];
      if(f) resumeFile.files = e.dataTransfer.files;
    });
  }


  /* -------------------------------
     DISPLAY CHAT MESSAGE
  ------------------------------- */

  function addMessage(text, who="ai"){
    const wrap = document.createElement("div");
    wrap.className = "msg " + (who === "user" ? "user" : "ai");

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = text;

    wrap.appendChild(bubble);
    chatWindow.appendChild(wrap);

    // auto-scroll
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }



  /* -------------------------------
        SEND CHAT MESSAGE
  ------------------------------- */

  chatForm && chatForm.addEventListener("submit", async (e)=>{
    e.preventDefault();

    const text = chatInput.value.trim();
    if(!text) return;

    // USER message
    addMessage(text, "user");
    chatInput.value = "";

    // send to backend
    const fd = new FormData();
    fd.append("message", text);

    try {
      const res = await fetch("/chat/send", { 
        method: "POST", 
        body: fd,
        credentials: "include"    // FIXED → sends login session cookie
      });

      const html = await res.text();

      const tmp = document.createElement("div");
      tmp.innerHTML = html;

      const content = tmp.textContent || tmp.innerText || "No reply";
      addMessage(content, "ai");

    } catch(err){
      addMessage("⚠️ Network issue. Please try again.", "ai");
    }
  });



  /* -------------------------------
       RESUME UPLOAD HANDLER
  ------------------------------- */

  uploadBtn && uploadBtn.addEventListener("click", async ()=>{

    const f = resumeFile.files[0];

    if(!f){ 
      addMessage("❗ Please choose a PDF file to upload.", "ai"); 
      return; 
    }

    if(f.type !== "application/pdf"){ 
      addMessage("❗ Only PDF files are supported.", "ai"); 
      return; 
    }

    uploadBtn.disabled = true;
    uploadBtn.textContent = "Uploading...";

    const fd = new FormData();
    fd.append("file", f);

    try {
      const res = await fetch("/upload-resume", { 
        method: "POST",
        body: fd,
        credentials: "include"   // FIXED → sends cookie, avoids 401 Unauthorized
      });

      if(!res.ok){
        addMessage("❌ Upload failed. Please login again.", "ai");
      } else {
        addMessage("✅ Resume uploaded & analyzed! Check Dashboard.", "ai");
      }

    } catch(err){
      addMessage("⚠️ Upload failed (network).", "ai");

    } finally {
      uploadBtn.disabled = false;
      uploadBtn.textContent = "Upload & Analyze";
    }

  });

});
