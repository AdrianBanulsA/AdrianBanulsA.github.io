// Some browsers open SVG links in a new tab even with the download attribute.
// Fetching the file and saving it as a generic blob forces a real download.
document.addEventListener("click", function (e) {
  var link = e.target.closest("a.qr-download");
  if (!link) return;
  e.preventDefault();
  fetch(link.href)
    .then(function (r) { return r.blob(); })
    .then(function (blob) {
      var url = URL.createObjectURL(new Blob([blob], { type: "application/octet-stream" }));
      var a = document.createElement("a");
      a.href = url;
      a.download = link.getAttribute("download");
      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
    })
    .catch(function () { location.href = link.href; });
});
