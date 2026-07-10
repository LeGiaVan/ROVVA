/**
 * Rovva customer — tương tác UI tối giản.
 *
 * Phần lớn dữ liệu đã được render server-side (Jinja + Flask). File này chỉ giữ
 * lại một số tương tác nhỏ phía client để giao diện mượt hơn.
 */

(function () {
  "use strict";

  // Tự ẩn thông báo flash sau vài giây.
  function autoDismissAlerts() {
    document.querySelectorAll(".alert-dismissible, [data-rova-flash]").forEach(function (el) {
      window.setTimeout(function () {
        el.classList.add("fade");
        el.style.transition = "opacity .4s ease";
        el.style.opacity = "0";
        window.setTimeout(function () { el.remove(); }, 400);
      }, 4000);
    });
  }

  // Nút yêu thích: chỉ đổi trạng thái hiển thị (demo). Dữ liệu thật quản lý ở server.
  function bindFavoriteButtons() {
    document.querySelectorAll(".favorite-btn").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        e.stopPropagation();
        var icon = btn.querySelector("i");
        if (!icon) return;
        var active = icon.classList.toggle("bi-heart-fill");
        icon.classList.toggle("bi-heart", !active);
        btn.classList.toggle("text-danger", active);
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    autoDismissAlerts();
    bindFavoriteButtons();
  });
})();
