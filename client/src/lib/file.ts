export interface Base64File {
  name: string;
  type: string;
  size: number;
  base64: string;
}

export function base64ToFile(base64: string, filename = "file", mimeType?: string): File {
  const arr = base64.split(",");
  let mime = mimeType || "application/octet-stream";
  let bstr: string;
  let dataUrl: string;

  if (arr.length === 2) {
    // data URL format: "data:mime/type;base64,XXXX"
    const extractedMime = arr[0].match(/:(.*?);/)?.[1];
    // Use provided mimeType if available, otherwise extract from data URL, otherwise fallback
    mime = mimeType || extractedMime || mime;
    dataUrl = base64; // Keep the original data URL

    // Set filename by mime (if generic 'file')
    if (filename === "file") {
      if (mime.startsWith("image/")) filename = "image.jpg";
      else if (mime === "application/pdf") filename = "document.pdf";
      else filename = "file.bin";
    }
    bstr = atob(arr[1]);
  } else {
    // Raw base64 string - use provided mimeType or infer from filename
    bstr = atob(base64);
    
    // If no mimeType provided, try to infer from filename extension
    if (!mimeType) {
      const ext = filename.toLowerCase().split('.').pop();
      if (ext === 'pdf') {
        mime = "application/pdf";
      } else if (['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg', 'bmp'].includes(ext || '')) {
        mime = `image/${ext === 'jpg' ? 'jpeg' : ext}`;
      } else {
        // Default to image/jpeg only if filename is generic "file" or "image.jpg"
        mime = (filename === "file" || filename === "image.jpg") ? "image/jpeg" : "application/octet-stream";
      }
    }
    
    if (filename === "file") {
      if (mime.startsWith("image/")) filename = "image.jpg";
      else if (mime === "application/pdf") filename = "document.pdf";
      else filename = "file.bin";
    }
    dataUrl = `data:${mime};base64,${base64}`;
  }

  let n = bstr.length;
  const u8arr = new Uint8Array(n);
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }

  const file = new File([u8arr], filename, { type: mime });

  // Use data URL for preview - this persists across page refreshes
  if (mime.startsWith("image/") || mime === "application/pdf") {
    Object.assign(file, {
      preview: dataUrl
    });
  }
  return file;
}

/**
 * Converts a File object to a strict/safe base64 encoding suitable for server actions.
 * Result: always outputs { name, type, size, base64: base64OnlyString }, base64 contains ONLY base64 payload (no data: prefix), binary-safe.
 * Chrome bug note: For binary, always use ArrayBuffer not text.
 */
export function fileToBase64(file: File): Promise<Base64File> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();

    reader.onload = () => {
      const result = reader.result as string;
      // result looks like: "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQ..."
      const base64 = result.split(",")[1]; // strip prefix for cleaner payload
      resolve({
        name: file.name,
        type: file.type,
        size: file.size,
        base64,
      });
    };

    reader.onerror = reject;
    reader.readAsDataURL(file); // ✅ Safe and universal
  });
}