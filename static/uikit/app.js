document.addEventListener("DOMContentLoaded", function () {
  // Highlight nếu có hljs
  if (window.hljs) hljs.highlightAll();

  // Lấy tất cả alert và nút đóng
  const alertWrappers = document.querySelectorAll(".custom-alert");
  const alertCloses = document.querySelectorAll(".custom-alert__close");

  alertCloses.forEach((btn) => {
    btn.addEventListener("click", () => {
      // Tìm alert cha gần nhất và xoá nó
      const alert = btn.closest(".custom-alert");
      if (alert) alert.remove();
    });
  });
});
