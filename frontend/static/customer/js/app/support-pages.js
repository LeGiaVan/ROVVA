/**
 * Nội dung tĩnh & tương tác cho các trang hỗ trợ / marketing (FAQ, đặc quyền, hướng dẫn, chính sách, AI).
 */

function escapeHtml(text) {
  return String(text)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

/* ── FAQ ───────────────────────────────────────────────────────────── */

var FAQ_GROUPS = [
  {
    num: 1,
    title: "Đặt phòng và Hủy đặt phòng",
    icon: "bi-calendar-check",
    color: "#2784F0",
    items: [
      {
        q: "Làm thế nào để tôi tiến hành đặt phòng trên hệ thống?",
        a: "Truy cập trang chủ Rovva, nhập điểm đến, ngày nhận/trả phòng và số khách. Nhấn Tìm kiếm, chọn cơ sở lưu trú phù hợp, điền thông tin liên hệ và hoàn tất thanh toán theo hướng dẫn.",
      },
      {
        q: "Tôi có thể thay đổi ngày lưu trú hoặc hủy đặt phòng đã đặt không?",
        a: "Có. Vào Chuyến đi của tôi, chọn đơn cần thay đổi. Tùy chính sách của từng chỗ nghỉ, bạn có thể đổi ngày hoặc hủy và nhận hoàn tiền theo mức quy định.",
      },
      {
        q: "Làm sao để biết thao tác đặt phòng của tôi đã thành công?",
        a: "Sau khi thanh toán thành công, hệ thống hiển thị màn hình xác nhận và gửi email kèm mã đặt phòng. Bạn cũng xem lại trong mục Chuyến đi của tôi.",
      },
    ],
  },
  {
    num: 2,
    title: "Thanh toán và Hóa đơn",
    icon: "bi-credit-card",
    color: "#16A34A",
    items: [
      {
        q: "Hệ thống hiện đang hỗ trợ những hình thức thanh toán nào?",
        a: "Rovva hỗ trợ chuyển khoản ngân hàng, thẻ nội địa/quốc tế, ví điện tử và thanh toán tại chỗ nghỉ (nếu chỗ nghỉ cho phép).",
      },
      {
        q: "Giá phòng hiển thị trên website đã bao gồm thuế và phí chưa?",
        a: "Giá hiển thị đã bao gồm thuế VAT cơ bản. Một số phí phát sinh tại chỗ (phí giường phụ, dọn phòng muộn…) sẽ được ghi rõ trước khi bạn xác nhận đặt phòng.",
      },
      {
        q: "Tôi đi công tác và cần xuất hóa đơn đỏ (VAT) thì phải làm sao?",
        a: "Khi đặt phòng, tick mục Yêu cầu xuất hóa đơn và điền đầy đủ thông tin công ty. Hóa đơn điện tử sẽ gửi qua email trong 3–7 ngày làm việc sau khi trả phòng.",
      },
    ],
  },
  {
    num: 3,
    title: "Nhận phòng và Trả phòng",
    icon: "bi-key",
    color: "#EA580C",
    items: [
      {
        q: "Khung giờ nhận phòng và trả phòng tiêu chuẩn là mấy giờ?",
        a: "Thông thường nhận phòng từ 14:00 và trả phòng trước 12:00. Giờ cụ thể có thể khác tùy từng cơ sở — xem trong email xác nhận hoặc trang chi tiết đặt phòng.",
      },
      {
        q: "Tôi có thể yêu cầu nhận phòng sớm hoặc trả phòng muộn được không?",
        a: "Có thể, tùy tình trạng phòng trống. Liên hệ lễ tân hoặc gửi yêu cầu qua Rovva trước ngày nhận phòng. Phí phát sinh (nếu có) sẽ được thông báo trước.",
      },
      {
        q: "Khi đến quầy lễ tân, tôi cần xuất trình những giấy tờ gì?",
        a: "CMND/CCCD hoặc hộ chiếu của người đặt phòng, mã đặt phòng Rovva và thẻ thanh toán (nếu cần đặt cọc tại chỗ).",
      },
    ],
  },
  {
    num: 4,
    title: "Tài khoản và Ưu đãi",
    icon: "bi-shield-check",
    color: "#7C3AED",
    items: [
      {
        q: "Làm cách nào để tôi sử dụng mã giảm giá (Voucher/Coupon)?",
        a: "Tại bước thanh toán, nhập mã vào ô Mã giảm giá và nhấn Áp dụng. Mã hợp lệ sẽ tự động trừ vào tổng tiền.",
      },
      {
        q: "Tôi quên mật khẩu đăng nhập tài khoản, làm cách nào để khôi phục?",
        a: "Nhấn Quên mật khẩu tại trang đăng nhập, nhập email đã đăng ký. Hệ thống gửi link đặt lại mật khẩu trong vài phút.",
      },
    ],
  },
  {
    num: 5,
    title: "Tiện ích và Dịch vụ",
    icon: "bi-stars",
    color: "#0891B2",
    items: [
      {
        q: "Khách sạn có hỗ trợ kê thêm giường phụ (Extra bed) hoặc có chính sách riêng cho trẻ em không?",
        a: "Tùy từng chỗ nghỉ. Xem mục Tiện ích & Chính sách trẻ em trên trang chi tiết, hoặc ghi chú yêu cầu khi đặt phòng.",
      },
      {
        q: "Nơi lưu trú có cung cấp dịch vụ xe đưa đón sân bay không và tôi đăng ký như thế nào?",
        a: "Nhiều đối tác có dịch vụ đưa đón. Chọn thêm dịch vụ tại bước điền thông tin hoặc liên hệ lễ tân sau khi đặt phòng thành công.",
      },
    ],
  },
  {
    num: 6,
    title: "Trở thành Host",
    icon: "bi-house-door",
    color: "#92400E",
    items: [
      {
        q: "Tôi có nhà trống, căn hộ hoặc khách sạn và muốn đăng cho thuê trên nền tảng thì phải làm sao?",
        a: "Truy cập mục Trở thành Host, điền hồ sơ đăng ký. Đội ngũ Rovva sẽ liên hệ hướng dẫn niêm yết và kết nối công cụ quản lý phòng.",
      },
      {
        q: "Việc đăng ký niêm yết chỗ nghỉ trên nền tảng có mất phí không?",
        a: "Đăng ký và niêm yết miễn phí. Rovva chỉ thu hoa hồng khi có đơn đặt phòng thành công qua hệ thống.",
      },
    ],
  },
];

function renderFaq() {
  var root = document.getElementById("faq-root");
  if (!root) return;

  var html = FAQ_GROUPS.map(function (group, gi) {
    var items = group.items.map(function (item, ii) {
      var id = "faq-" + gi + "-" + ii;
      return (
        '<div class="faq-item">' +
        '<button class="faq-item__question collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#' + id + '" aria-expanded="false">' +
        "<span>" + escapeHtml(item.q) + '</span><i class="bi bi-chevron-down"></i></button>' +
        '<div class="collapse" id="' + id + '" data-bs-parent="#faq-acc-' + gi + '">' +
        '<div class="faq-item__answer">' + escapeHtml(item.a) + "</div></div></div>"
      );
    }).join("");

    return (
      '<div class="faq-group">' +
      '<div class="faq-group__head" style="--faq-color:' + group.color + '">' +
      '<span class="faq-group__badge"><i class="bi ' + group.icon + '"></i></span>' +
      '<h3 class="faq-group__title">' + group.num + ". " + escapeHtml(group.title) + "</h3></div>" +
      '<div class="faq-list" id="faq-acc-' + gi + '">' + items + "</div></div>"
    );
  }).join("");

  root.innerHTML = html;
}

/* ── Privileges & promotions ───────────────────────────────────────── */

var TIER_CARDS = [
  {
    key: "member",
    cls: "tier-card--member",
    icon: "bi-person-badge",
    name: "Thành Viên",
    spend: "Mặc định khi đăng ký",
    perks: ["Tích 1% giá trị đơn", "Thanh toán tối đa 10% hóa đơn bằng Xu", "5 Xu khi viết đánh giá"],
  },
  {
    key: "silver",
    cls: "tier-card--silver",
    icon: "bi-award",
    name: "Hạng Bạc",
    spend: "Chi tiêu từ 3.000.000đ",
    perks: ["Tích 1% giá trị đơn", "Thanh toán tối đa 12% hóa đơn bằng Xu", "5 Xu khi viết đánh giá"],
  },
  {
    key: "gold",
    cls: "tier-card--gold",
    icon: "bi-star-fill",
    name: "Hạng Vàng",
    spend: "Chi tiêu từ 10.000.000đ",
    perks: ["Tích 1,2% giá trị đơn", "Thanh toán tối đa 15% hóa đơn bằng Xu", "Gấp đôi Xu trong tháng sinh nhật", "5 Xu khi viết đánh giá"],
    featured: true,
  },
  {
    key: "platinum",
    cls: "tier-card--platinum",
    icon: "bi-gem",
    name: "Hạng Bạch Kim",
    spend: "Chi tiêu từ 25.000.000đ",
    perks: ["Tích 1,5% giá trị đơn", "Thanh toán tối đa 15% hóa đơn bằng Xu", "Gấp ba Xu trong tháng sinh nhật", "10 Xu khi viết đánh giá"],
  },
];

var VOUCHERS = [
  { tier: "all", discount: "50.000đ", title: "Giảm ngay 50.000đ", cond: "Đơn từ 800.000đ", expiry: "31/07/2026" },
  { tier: "all", discount: "7%", title: "Giảm 7% (Tối đa 150.000đ)", cond: "Áp dụng mọi loại hình", expiry: "31/08/2026" },
  { tier: "silver", discount: "100.000đ", title: "Ưu đãi Hạng Bạc", cond: "Dành cho hạng Bạc trở lên", expiry: "30/09/2026" },
  { tier: "gold", discount: "12%", title: "Giảm 12% (Tối đa 300.000đ)", cond: "Hạng Vàng trở lên", expiry: "15/10/2026" },
  { tier: "platinum", discount: "200.000đ", title: "Đặc quyền Bạch Kim", cond: "Đơn từ 2.000.000đ", expiry: "31/12/2026" },
  { tier: "gold", discount: "80.000đ", title: "Flash sale cuối tuần", cond: "Thứ 6–CN hàng tuần", expiry: "31/07/2026" },
  { tier: "silver", discount: "5%", title: "Giảm 5% đặt sớm", cond: "Đặt trước 14 ngày", expiry: "30/11/2026" },
  { tier: "platinum", discount: "15%", title: "Giảm 15% resort cao cấp", cond: "Tối đa 500.000đ", expiry: "28/02/2027" },
];

function renderPrivileges() {
  var root = document.getElementById("privileges-root");
  if (!root) return;

  var tiers = TIER_CARDS.map(function (t) {
    var perks = t.perks.map(function (p) { return "<li>" + escapeHtml(p) + "</li>"; }).join("");
    return (
      '<article class="tier-card ' + t.cls + (t.featured ? " tier-card--featured" : "") + '">' +
      '<div class="tier-card__head"><span class="tier-card__icon"><i class="bi ' + t.icon + '"></i></span>' +
      '<h3 class="tier-card__name">' + escapeHtml(t.name) + "</h3></div>" +
      '<dl class="tier-card__specs"><dt>Điều kiện</dt><dd>' + escapeHtml(t.spend) + "</dd></dl>" +
      '<div class="tier-card__perks"><span class="tier-card__perks-label">Quyền lợi</span><ul>' + perks + "</ul></div></article>"
    );
  }).join("");

  var vouchers = VOUCHERS.map(function (v, i) {
    return (
      '<div class="col-sm-6 col-lg-3 promo-voucher-col" data-voucher-tier="' + v.tier + '">' +
      '<article class="promo-voucher h-100">' +
      '<div class="promo-voucher__left"><span class="promo-voucher__brand">ROVVA</span></div>' +
      '<div class="promo-voucher__body">' +
      '<div class="promo-voucher__discount">' + escapeHtml(v.discount) + "</div>" +
      '<h4 class="promo-voucher__title">' + escapeHtml(v.title) + "</h4>" +
      '<p class="promo-voucher__cond">' + escapeHtml(v.cond) + "</p>" +
      '<div class="promo-voucher__foot">' +
      '<span class="promo-voucher__expiry">Hạn dùng: ' + escapeHtml(v.expiry) + "</span>" +
      '<button type="button" class="btn btn-sm btn-light promo-voucher__claim">Nhận mã</button>' +
      "</div></div></article></div>"
    );
  }).join("");

  root.innerHTML =
    '<section class="mb-5">' +
    '<h2 class="promo-section-title">Hệ thống cấp bậc thành viên</h2>' +
    '<p class="text-muted mb-4">Đăng ký tài khoản Rovva để mở khóa ưu đãi, tích Xu và nâng hạng theo tổng chi tiêu hợp lệ.</p>' +
    '<div class="tier-carousel-wrap"><div class="tier-carousel"><div class="tier-carousel__viewport">' +
    '<div class="tier-carousel__track">' + tiers + "</div></div></div></div></section>" +
    '<section class="mb-5">' +
    '<h2 class="promo-section-title">Quy tắc cấp bậc thành viên</h2>' +
    '<ul class="tier-rules">' +
    "<li><strong>Chu kỳ ghi nhận:</strong> 12 tháng, xét lại hạng vào đầu mỗi năm dương lịch.</li>" +
    "<li><strong>Trạng thái đơn hợp lệ:</strong> Chỉ đơn Hoàn tất (check-out thành công) được tính vào tổng chi tiêu.</li>" +
    "<li><strong>Duy trì và rớt hạng:</strong> Nếu không đạt ngưỡng chi tiêu của hạng hiện tại, hạng sẽ điều chỉnh theo mức tương ứng vào chu kỳ kế tiếp.</li>" +
    "</ul></section>" +
    '<section class="mb-4">' +
    '<h2 class="promo-section-title">Kho voucher đặc quyền</h2>' +
    '<div class="promo-filter" id="promo-voucher-filter">' +
    '<button type="button" class="promo-filter__chip is-active" data-tier="all">Tất cả</button>' +
    '<button type="button" class="promo-filter__chip" data-tier="silver">Hạng Bạc</button>' +
    '<button type="button" class="promo-filter__chip" data-tier="gold">Hạng Vàng</button>' +
    '<button type="button" class="promo-filter__chip" data-tier="platinum">Hạng Bạch Kim</button>' +
    "</div>" +
    '<div class="row g-3" id="promo-voucher-grid">' + vouchers + "</div></section>";

  var filter = document.getElementById("promo-voucher-filter");
  if (filter) {
    filter.addEventListener("click", function (e) {
      var chip = e.target.closest("[data-tier]");
      if (!chip) return;
      filter.querySelectorAll(".promo-filter__chip").forEach(function (c) {
        c.classList.toggle("is-active", c === chip);
      });
      var tier = chip.getAttribute("data-tier");
      document.querySelectorAll("[data-voucher-tier]").forEach(function (col) {
        var show = tier === "all" || col.getAttribute("data-voucher-tier") === tier;
        col.style.display = show ? "" : "none";
      });
    });
  }

  root.querySelectorAll(".promo-voucher__claim").forEach(function (btn) {
    btn.addEventListener("click", function () {
      btn.textContent = "Đã nhận";
      btn.disabled = true;
      btn.classList.add("disabled");
    });
  });
}

/* ── Booking / cancel guides ───────────────────────────────────────── */

var GUIDE_BOOKING = [
  {
    badge: "BƯỚC 1",
    icon: "bi-search",
    title: "Tìm kiếm chỗ nghỉ",
    points: [
      "Truy cập trang chủ Rovva, nhập điểm đến, ngày nhận/trả phòng và số khách.",
      "Nhấn [Tìm kiếm] để xem danh sách cơ sở lưu trú phù hợp.",
    ],
  },
  {
    badge: "BƯỚC 2",
    icon: "bi-building",
    title: "Lựa chọn cơ sở lưu trú",
    points: [
      "Dùng bộ lọc (giá, tiện ích, vị trí) để thu hẹp kết quả.",
      "Nhấn vào từng chỗ nghỉ để xem ảnh, đánh giá và chọn phòng.",
      "Nhấn [Đặt phòng ngay] khi đã chọn được phòng ưng ý.",
    ],
  },
  {
    badge: "BƯỚC 3",
    icon: "bi-card-text",
    title: "Điền thông tin",
    points: [
      "Nhập họ tên, email, số điện thoại của người đặt.",
      "Thêm dịch vụ bổ sung (đưa đón, spa…) nếu cần.",
      "Áp dụng mã giảm giá hoặc Xu thưởng (nếu có).",
    ],
  },
  {
    badge: "BƯỚC 4",
    icon: "bi-check-circle",
    title: "Thanh toán & Nhận xác nhận",
    points: [
      "Kiểm tra tổng chi phí và chọn hình thức thanh toán.",
      "Với thanh toán online: làm theo hướng dẫn và xác nhận đã chuyển khoản.",
      "Với thanh toán tại chỗ: hệ thống hoàn tất đặt phòng ngay.",
      "Email xác nhận kèm mã đặt phòng sẽ được gửi đến bạn.",
    ],
  },
];

var GUIDE_CANCEL = [
  {
    badge: "BƯỚC 1",
    icon: "bi-person",
    title: "Truy cập Chuyến đi của tôi",
    points: [
      "Đăng nhập vào tài khoản Rovva.",
      "Chọn mục Chuyến đi của tôi trong menu Tài khoản.",
    ],
  },
  {
    badge: "BƯỚC 2",
    icon: "bi-journal-text",
    title: "Chọn đơn đặt phòng cần hủy",
    points: [
      "Tại tab Sắp tới, tìm đơn bạn muốn hủy.",
      "Nhấn nút [Hủy đặt phòng] trên thẻ thông tin đơn.",
    ],
  },
  {
    badge: "BƯỚC 3",
    icon: "bi-shield-exclamation",
    title: "Kiểm tra chính sách & Xác nhận",
    points: [
      "Đọc kỹ chính sách hoàn tiền hiển thị trên màn hình.",
      "Chọn lý do hủy và nhấn [Xác nhận hủy].",
    ],
  },
  {
    badge: "BƯỚC 4",
    icon: "bi-envelope-check",
    title: "Nhận thông báo hoàn tất",
    points: [
      "Đơn hàng chuyển sang tab Đã hủy.",
      "Email xác nhận hủy và thông tin hoàn tiền (nếu có) sẽ được gửi đến bạn.",
    ],
  },
];

function renderGuideSteps(steps) {
  return (
    '<ol class="guide-steps">' +
    steps.map(function (s) {
      var pts = s.points.map(function (p) { return "<li>" + escapeHtml(p) + "</li>"; }).join("");
      return (
        '<li class="guide-step">' +
        '<div class="guide-step__badge"><i class="bi ' + s.icon + ' d-block mb-1"></i>' + escapeHtml(s.badge) + "</div>" +
        '<div class="guide-step__body">' +
        '<h3 class="guide-step__title">' + escapeHtml(s.title) + "</h3>" +
        '<ul class="guide-step__points">' + pts + "</ul></div></li>"
      );
    }).join("") +
    "</ol>"
  );
}

function initGuide() {
  var root = document.getElementById("guide-root");
  if (!root) return;

  var defaultTab = document.body.getAttribute("data-guide-tab") || "booking";
  var isBooking = defaultTab === "booking";
  var bookingUrl = root.getAttribute("data-booking-url") || "#";
  var cancelUrl = root.getAttribute("data-cancel-url") || "#";

  root.innerHTML =
    '<nav class="guide-tabs mb-4" role="tablist">' +
    '<a class="guide-tab' + (isBooking ? " is-active" : "") + '" href="' + escapeHtml(bookingUrl) + '">Hướng dẫn Đặt phòng</a>' +
    '<a class="guide-tab' + (!isBooking ? " is-active" : "") + '" href="' + escapeHtml(cancelUrl) + '">Hướng dẫn Hủy đặt phòng</a>' +
    "</nav>" +
    '<div class="page-card">' +
    '<h2 class="guide-heading">' + (isBooking ? "Các bước Đặt phòng:" : "Các bước Hủy đặt phòng:") + "</h2>" +
    renderGuideSteps(isBooking ? GUIDE_BOOKING : GUIDE_CANCEL) +
    "</div>";
}

/* ── Policy pages ──────────────────────────────────────────────────── */

var POLICIES = {
  privacy: {
    title: "Chính sách bảo mật",
    updated: "01 tháng 6, 2024",
    intro: "Rovva cam kết bảo vệ quyền riêng tư của bạn. Chính sách này mô tả cách chúng tôi thu thập, sử dụng và bảo vệ dữ liệu cá nhân khi bạn sử dụng nền tảng Smart Stay.",
    sections: [
      {
        id: "scope",
        title: "1. Đối tượng và phạm vi áp dụng",
        html:
          '<p class="policy-text">Chính sách áp dụng cho <strong>Thành viên</strong> (đã đăng ký tài khoản) và <strong>Khách truy cập</strong> (sử dụng website mà chưa đăng nhập).</p>' +
          '<p class="policy-subheading">1.1 Thành viên</p><p class="policy-text">Người dùng đã tạo tài khoản và đặt phòng qua Rovva.</p>' +
          '<p class="policy-subheading">1.2 Khách truy cập</p><p class="policy-text">Người dùng xem thông tin, tìm kiếm hoặc trò chuyện với Trợ lý AI mà chưa đăng nhập.</p>',
      },
      {
        id: "data",
        title: "2. Loại dữ liệu thu thập",
        html:
          '<ul class="policy-list"><li>Thông tin định danh: họ tên, email, số điện thoại.</li>' +
          "<li>Dữ liệu giao dịch: lịch sử đặt phòng, thanh toán, hoàn tiền.</li>" +
          "<li>Dữ liệu tương tác AI: nội dung trò chuyện với Trợ lý Rovva AI để cải thiện dịch vụ.</li></ul>",
      },
      {
        id: "purpose",
        title: "3. Mục đích sử dụng dữ liệu",
        html:
          '<ul class="policy-list"><li>Xử lý đặt phòng, thanh toán và hỗ trợ khách hàng.</li>' +
          "<li>Cá nhân hóa gợi ý chỗ nghỉ và ưu đãi.</li>" +
          "<li>Huấn luyện và cải thiện Trợ lý AI (dữ liệu được ẩn danh hóa khi phù hợp).</li></ul>",
      },
      {
        id: "sharing",
        title: "4. Chia sẻ với bên thứ ba",
        html:
          '<p class="policy-text">Chúng tôi chỉ chia sẻ dữ liệu cần thiết với:</p>' +
          '<ul class="policy-list"><li>Host/đối tác lưu trú — thông tin đặt phòng để phục vụ lưu trú.</li>' +
          "<li>Đối tác thanh toán — xử lý giao dịch an toàn.</li></ul>",
      },
      {
        id: "security",
        title: "5. Lưu trữ và bảo mật",
        html:
          '<p class="policy-text">Dữ liệu được mã hóa trong quá trình truyền tải (SSL/TLS). Chúng tôi lưu trữ trong thời gian cần thiết để cung cấp dịch vụ và tuân thủ pháp luật.</p>',
      },
      {
        id: "rights",
        title: "6. Quyền của người dùng",
        html:
          '<ul class="policy-list"><li>Yêu cầu truy cập, chỉnh sửa hoặc xóa dữ liệu cá nhân.</li>' +
          "<li>Yêu cầu xóa lịch sử trò chuyện với Trợ lý AI.</li>" +
          "<li>Rút lại sự đồng ý marketing bất cứ lúc nào.</li></ul>",
      },
      {
        id: "cookies",
        title: "7. Chính sách Cookie",
        html:
          '<p class="policy-text">Rovva sử dụng cookie để ghi nhớ trạng thái đăng nhập, tùy chọn ngôn ngữ và phân tích lưu lượng. Bạn có thể tắt cookie trong trình duyệt nhưng một số tính năng có thể bị hạn chế.</p>',
      },
      {
        id: "contact",
        title: "8. Thông tin liên hệ",
        html:
          '<p class="policy-text">Mọi thắc mắc về bảo mật, vui lòng liên hệ:</p>' +
          '<ul class="policy-list"><li>Email: support@rovva.com</li><li>Hotline: 1900 2005</li>' +
          '<li>Biểu mẫu trực tuyến: mục Trợ giúp &amp; Yêu cầu trên website.</li></ul>',
      },
    ],
  },
  operation: {
    title: "Chính sách hoạt động",
    updated: "15 tháng 5, 2024",
    intro: "Chính sách hoạt động quy định nguyên tắc vận hành nền tảng Rovva, trách nhiệm giữa các bên và quy trình xử lý sự cố.",
    sections: [
      {
        id: "general",
        title: "1. Nguyên tắc chung",
        html: '<p class="policy-text">Rovva đóng vai trò nền tảng kết nối khách lưu trú và đối tác Host. Chúng tôi cam kết minh bạch giá, thông tin chỗ nghỉ và quy trình đặt/hủy phòng.</p>',
      },
      {
        id: "booking",
        title: "2. Quy trình đặt phòng",
        html:
          '<ul class="policy-list"><li>Giá và tình trạng phòng được cập nhật theo thời gian thực từ Host.</li>' +
          "<li>Đơn đặt chỉ có hiệu lực sau khi thanh toán/xác nhận thành công.</li>" +
          "<li>Email xác nhận là căn cứ chính thức cho việc nhận phòng.</li></ul>",
      },
      {
        id: "cancel",
        title: "3. Hủy đặt phòng & hoàn tiền",
        html:
          '<p class="policy-text">Chính sách hủy phụ thuộc từng chỗ nghỉ (Linh hoạt, Vừa phải, Nghiêm ngặt). Mức hoàn tiền hiển thị rõ trước khi bạn xác nhận hủy.</p>',
      },
      {
        id: "host",
        title: "4. Trách nhiệm đối tác Host",
        html:
          '<ul class="policy-list"><li>Cung cấp thông tin chính xác về phòng, tiện ích và giá.</li>' +
          "<li>Đảm bảo phòng sẵn sàng đúng thời gian đã đặt.</li>" +
          "<li>Phối hợp xử lý khiếu nại trong 24 giờ làm việc.</li></ul>",
      },
      {
        id: "customer",
        title: "5. Trách nhiệm khách hàng",
        html:
          '<ul class="policy-list"><li>Cung cấp thông tin liên hệ chính xác.</li>' +
          "<li>Tuân thủ nội quy chỗ nghỉ và giờ nhận/trả phòng.</li>" +
          "<li>Thanh toán đầy đủ các khoản phí phát sinh tại chỗ (nếu có).</li></ul>",
      },
      {
        id: "dispute",
        title: "6. Giải quyết tranh chấp",
        html:
          '<p class="policy-text">Khiếu nại gửi qua Trợ giúp &amp; Yêu cầu hoặc hotline. Rovva điều phối giữa khách và Host, phản hồi trong 3–5 ngày làm việc.</p>',
      },
      {
        id: "suspend",
        title: "7. Tạm ngưng tài khoản",
        html:
          '<p class="policy-text">Rovva có quyền tạm ngưng tài khoản vi phạm điều khoản, gian lận thanh toán hoặc hành vi gây hại cho cộng đồng.</p>',
      },
      {
        id: "changes",
        title: "8. Thay đổi chính sách",
        html:
          '<p class="policy-text">Chính sách có thể được cập nhật. Phiên bản mới sẽ công bố trên website kèm ngày hiệu lực.</p>',
      },
    ],
  },
  terms: {
    title: "Điều khoản & Điều kiện sử dụng",
    updated: "01 tháng 6, 2024",
    intro: "Bằng việc truy cập và sử dụng Rovva, bạn đồng ý tuân thủ các điều khoản dưới đây. Vui lòng đọc kỹ trước khi đặt phòng hoặc đăng ký tài khoản.",
    sections: [
      {
        id: "defs",
        title: "1. Định nghĩa",
        html:
          '<dl class="policy-defs">' +
          "<dt>Rovva / Chúng tôi</dt><dd>Công ty vận hành nền tảng Smart Stay Platform.</dd>" +
          "<dt>Người dùng / Bạn</dt><dd>Khách truy cập, thành viên hoặc Host sử dụng dịch vụ.</dd>" +
          "<dt>Dịch vụ</dt><dd>Website, ứng dụng, Trợ lý AI và các tính năng đặt phòng liên quan.</dd></dl>",
      },
      {
        id: "account",
        title: "2. Tài khoản",
        html:
          '<ul class="policy-list"><li>Bạn chịu trách nhiệm bảo mật mật khẩu và mọi hoạt động trên tài khoản.</li>' +
          "<li>Thông tin đăng ký phải trung thực và cập nhật.</li></ul>",
      },
      {
        id: "service",
        title: "3. Phạm vi dịch vụ",
        html:
          '<p class="policy-text">Rovva cung cấp công cụ tìm kiếm, đặt phòng và hỗ trợ. Hợp đồng lưu trú được ký giữa bạn và Host; Rovva là bên trung gian kết nối.</p>',
      },
      {
        id: "payment",
        title: "4. Thanh toán",
        html:
          '<ul class="policy-list"><li>Giá hiển thị tại thời điểm đặt là căn cứ thanh toán.</li>' +
          "<li>Phí chuyển đổi ngoại tệ (nếu có) do ngân hàng/đối tác thu.</li></ul>",
      },
      {
        id: "ip",
        title: "5. Sở hữu trí tuệ",
        html:
          '<p class="policy-text">Logo, giao diện, thuật toán AI và nội dung trên Rovva thuộc quyền sở hữu của chúng tôi. Nghiêm cấm sao chép trái phép.</p>',
      },
      {
        id: "liability",
        title: "6. Giới hạn trách nhiệm",
        html:
          '<p class="policy-text">Rovva không chịu trách nhiệm cho thiệt hại gián tiếp. Trách nhiệm tối đa trong phạm vi pháp luật cho phép bằng giá trị đơn đặt phòng liên quan.</p>',
      },
      {
        id: "law",
        title: "7. Luật áp dụng",
        html:
          '<p class="policy-text">Điều khoản được điều chỉnh theo pháp luật Việt Nam. Tranh chấp ưu tiên giải quyết thương lượng, hòa giải trước khi đưa ra tòa án có thẩm quyền tại TP. Hồ Chí Minh.</p>',
      },
      {
        id: "contact-terms",
        title: "8. Liên hệ",
        html:
          '<p class="policy-text">Email: support@rovva.com · Hotline: 1900 2005 · Địa chỉ: The Sarus Building, 67 Nguyễn Thị Minh Khai, Q.1, TP.HCM.</p>',
      },
    ],
  },
};

function renderPolicy() {
  var key = document.body.getAttribute("data-policy");
  if (!key || !POLICIES[key]) return;
  var root = document.getElementById("policy-root");
  if (!root) return;

  var policy = POLICIES[key];
  var homeUrl = root.getAttribute("data-home-url") || "/";

  var toc = policy.sections.map(function (s, i) {
    return (
      '<a class="policy-toc__link' + (i === 0 ? " is-active" : "") + '" href="#' + s.id + '" data-policy-link="' + s.id + '">' +
      escapeHtml(s.title) + "</a>"
    );
  }).join("");

  var sections = policy.sections.map(function (s) {
    return (
      '<section class="policy-section" id="' + s.id + '">' +
      '<h2 class="policy-heading">' + escapeHtml(s.title) + "</h2>" + s.html + "</section>"
    );
  }).join("");

  root.innerHTML =
    '<section class="policy-hero"><div class="container-xxl">' +
    '<h1 class="policy-hero__title">' + escapeHtml(policy.title) + "</h1>" +
    '<p class="policy-hero__intro">' + escapeHtml(policy.intro) + "</p>" +
    '<p class="policy-hero__updated">Cập nhật lần cuối: ' + escapeHtml(policy.updated) + "</p></div></section>" +
    '<div class="container-xxl"><div class="policy-layout">' +
    '<aside class="policy-toc"><h2 class="policy-toc__title">Mục lục chính sách</h2><nav class="policy-toc__nav">' + toc + "</nav></aside>" +
    '<div class="policy-content">' + sections +
    '<div class="policy-back"><a class="btn btn-rova-primary" href="' + escapeHtml(homeUrl) + '"><i class="bi bi-house"></i> Quay lại Trang chủ</a></div>' +
    "</div></div></div>";

  var links = root.querySelectorAll("[data-policy-link]");
  links.forEach(function (link) {
    link.addEventListener("click", function () {
      links.forEach(function (l) { l.classList.remove("is-active"); });
      link.classList.add("is-active");
    });
  });
}

/* ── Help form ─────────────────────────────────────────────────────── */

function initHelpForm() {
  var form = document.getElementById("help-request-form");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var btn = form.querySelector('[type="submit"]');
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = '<i class="bi bi-check-circle"></i> Đã gửi yêu cầu';
    }
    window.setTimeout(function () {
      form.reset();
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-send"></i> Gửi yêu cầu hỗ trợ';
      }
    }, 3000);
  });
}

/* ── Blog filters ──────────────────────────────────────────────────── */

function initBlogFilters() {
  var chips = document.querySelectorAll(".blog-filter__chip");
  var cards = document.querySelectorAll("#blog-grid .col-sm-6");
  if (!chips.length || !cards.length) return;

  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      chips.forEach(function (c) { c.classList.remove("is-active"); });
      chip.classList.add("is-active");
      var label = chip.textContent.trim();
      cards.forEach(function (col) {
        if (label === "Tất cả") {
          col.style.display = "";
          return;
        }
        var meta = col.querySelector(".blog-card__meta span");
        var show = meta && meta.textContent.indexOf(label) !== -1;
        col.style.display = show ? "" : "none";
      });
    });
  });
}

/* ── AI chat (demo) ────────────────────────────────────────────────── */

var AI_REPLIES = {
  "gợi ý": "Bạn có thể thử Đà Lạt, Phú Quốc hoặc Đà Nẵng — mỗi nơi đều có homestay và resort được đánh giá cao trên Rovva. Bạn muốn đi mấy ngày và đi cùng ai?",
  "khách sạn": "Tôi gợi ý lọc theo khu vực trung tâm và đánh giá từ 4 sao trở lên. Bạn cho tôi biết ngân sách/đêm để tìm chính xác hơn nhé!",
  "ưu đãi": "Thành viên mới có voucher giảm 50.000đ cho đơn đầu tiên. Đăng ký tài khoản và xem thêm tại mục Đặc quyền & Khuyến mãi.",
  "hỗ trợ": "Bạn có thể gọi hotline 1900 2005 hoặc gửi yêu cầu tại Trợ giúp & Yêu cầu. Tôi cũng có thể hướng dẫn hủy/đổi đặt phòng ngay bây giờ.",
  "đặt phòng": "Vào Chuyến đi của tôi để xem, đổi hoặc hủy đơn. Bạn cần mã đặt phòng cụ thể không?",
  default: "Cảm ơn bạn! Tôi đã ghi nhận yêu cầu. Bạn có thể mô tả thêm điểm đến, ngày đi hoặc ngân sách để tôi gợi ý chi tiết hơn.",
};

function aiReplyFor(text) {
  var lower = text.toLowerCase();
  var keys = Object.keys(AI_REPLIES);
  for (var i = 0; i < keys.length; i++) {
    if (keys[i] !== "default" && lower.indexOf(keys[i]) !== -1) {
      return AI_REPLIES[keys[i]];
    }
  }
  return AI_REPLIES.default;
}

function appendAiMessage(container, role, text) {
  var el = document.createElement("div");
  el.className = role === "user" ? "ai-msg ai-msg--user" : "ai-msg ai-msg--bot";
  el.innerHTML = "<p>" + escapeHtml(text) + "</p>";
  container.appendChild(el);
  container.scrollTop = container.scrollHeight;
}

function initAiChat() {
  var shell = document.querySelector(".ai-shell");
  if (!shell) return;

  var messages = document.getElementById("ai-messages");
  var welcome = document.getElementById("ai-welcome");
  var form = document.getElementById("ai-chat-form");
  var input = form ? form.querySelector("input") : null;

  function send(text) {
    if (!text || !messages) return;
    if (welcome) welcome.style.display = "none";
    appendAiMessage(messages, "user", text);
    window.setTimeout(function () {
      appendAiMessage(messages, "bot", aiReplyFor(text));
    }, 600);
  }

  if (form && input) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var val = input.value.trim();
      if (!val) return;
      send(val);
      input.value = "";
    });
  }

  document.querySelectorAll(".ai-suggestion").forEach(function (btn) {
    btn.addEventListener("click", function () {
      send(btn.getAttribute("data-prompt") || btn.textContent.trim());
    });
  });

  var newChat = document.getElementById("ai-new-chat");
  if (newChat && messages) {
    newChat.addEventListener("click", function () {
      messages.querySelectorAll(".ai-msg").forEach(function (m) { m.remove(); });
      if (welcome) welcome.style.display = "";
    });
  }
}

/* ── Entry ─────────────────────────────────────────────────────────── */

export function initSupportPages() {
  renderFaq();
  renderPrivileges();
  initGuide();
  renderPolicy();
  initHelpForm();
  initBlogFilters();
  initAiChat();
}
