# Báo Cáo Nhóm — Lab 7: Embedding & Vector Store

**Nhóm:** G23
**Thành viên:** Mai Hoàng Anh, Hoàng Văn Sơn, Phan Danh Đạt
**Ngày:** 20/09/2026

> **Nộp 1 bản / nhóm.** Phần cá nhân (hướng tiếp cận, kết quả riêng, dự đoán…) mỗi thành viên nộp riêng trong `REPORT_CANHAN.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần nhóm: 40** = Lựa chọn tài liệu (10) + Thiết kế chiến lược (15) + Chất lượng truy xuất (10) + Thuyết trình (5).

---

## 1. Lựa chọn tài liệu (Document Set Quality) — Nhóm (10 điểm)

### Chủ đề (Domain) & Lý Do Chọn

**Chủ đề:** Chính sách đơn hàng Shopee

**Tại sao nhóm chọn chủ đề này?**
Nhóm chọn chủ đề này vì Shopee là một sàn thương mại điện tử phổ biến tại Việt Nam, có nhiều chính sách phức tạp liên quan đến đơn hàng, giao hàng, thanh toán, trả hàng, hoàn tiền, hủy đơn hàng, v.v. Các chính sách này thường thay đổi theo thời gian, do đó việc cập nhật và quản lý thông tin chính sách là rất quan trọng đối với người dùng. Hơn nữa, các chính sách này thường được trình bày dưới dạng văn bản dài, do đó việc áp dụng các kỹ thuật xử lý ngôn ngữ tự nhiên để trích xuất và tóm tắt thông tin là rất phù hợp.

### Danh sách tài liệu (Data Inventory)

| # | Tài liệu trong corpus | Source URL | Ký tự phần thân | Metadata audience / category |
|---|---|---|---:|---|
| 1 | [Xem trạng thái đơn mua Shopee](../data/shopee-orders/buyer-order-status.md) | [Bài chính thức](https://help.shopee.vn/portal/4/article/79472) | 578 | `buyer` / `order-status` |
| 2 | [Điều kiện người mua yêu cầu hủy đơn](../data/shopee-orders/buyer-cancel-order.md) | [Bài chính thức](https://help.shopee.vn/portal/4/article/79182) | 732 | `buyer` / `cancellation` |
| 3 | [Đơn đã hủy và các nguyên nhân thường gặp](../data/shopee-orders/buyer-cancelled-order.md) | [Bài chính thức](https://help.shopee.vn/portal/4/article/79519-%5BH%E1%BB%A7y-%C4%91%C6%A1n-h%C3%A0ng%5D-T%C3%B4i-c%C3%B3-th%E1%BB%83-kh%C3%B4i-ph%E1%BB%A5c-l%E1%BA%A1i-%C4%91%C6%A1n-h%C3%A0ng-%C4%91%C3%A3-h%E1%BB%A7y-T%E1%BA%A1i-sao-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-l%E1%BA%A1i-b%E1%BB%8B-h%E1%BB%A7y) | 593 | `buyer` / `cancelled-order` |
| 4 | [Hạn thanh toán đơn trả trước](../data/shopee-orders/buyer-prepayment.md) | [Bài chính thức](https://help.shopee.vn/portal/4/article/79473-%5BPh%C6%B0%C6%A1ng-th%E1%BB%A9c-thanh-to%C3%A1n%5D-T%C3%B4i-c%E1%BA%A7n-ho%C3%A0n-t%E1%BA%A5t-thanh-to%C3%A1n-nh%E1%BB%AFng-%C4%91%C6%A1n-h%C3%A0ng-tr%E1%BA%A3-tr%C6%B0%E1%BB%9Bc-trong-bao-l%C3%A2u) | 550 | `buyer` / `payment-deadline` |
| 5 | [Tra cứu đơn trong phần trò chuyện Shopee](../data/shopee-orders/buyer-track-chat.md) | [Bài chính thức](https://help.shopee.vn/portal/4/article/79600) | 455 | `buyer` / `order-tracking` |
| 6 | [Người bán phản hồi yêu cầu hủy](../data/shopee-orders/seller-cancel-request.md) | [Bài chính thức](https://help.shopee.vn/portal/1/article/98754) | 615 | `seller` / `cancellation` |
| 7 | [Theo dõi kiện giao thất bại và hàng hoàn](../data/shopee-orders/seller-failed-delivery.md) | [Bài chính thức](https://help.shopee.vn/portal/1/article/102523) | 612 | `seller` / `failed-delivery` |


**Danh sách kiểm tra quản trị dữ liệu (Data governance checklist):**
- [X] Tập tài liệu (Corpus) chỉ chứa nguồn công khai/được phép dùng và không chứa dữ liệu cá nhân, thông tin đăng nhập hoặc tài liệu nội bộ.
- [X] Mỗi tài liệu có `source_url`, `retrieved_at`, `document_version` (hoặc ngày hiệu lực) trong metadata.

### Cấu trúc Metadata (Metadata Schema)

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho truy xuất (retrieval)? |
| --- | --- | --- | --- |
| `doc_id`, `title` | Chuỗi | `buyer-cancel-order` | Nhận diện tài liệu gốc, kiểm tra và xóa toàn bộ chunk của tài liệu |
| `source_url`, `source_section` | Chuỗi | URL và mục nguồn | Dẫn nguồn, chỉ ra phần đã được tóm lược |
| `retrieved_at`, `document_version` | Chuỗi | `2026-09-20`, `not-stated` | Phân biệt ngày thu thập với ngày hiệu lực |
| `audience` | Chuỗi | `buyer` hoặc `seller` | Lọc theo vai trò trước khi xếp hạng |
| `category` | Chuỗi | `cancellation`, `payment-deadline` | Nhận diện chủ đề, có thể mở rộng bộ lọc |
| `language`, `platform` | Chuỗi | `vi`, `shopee` | Phân biệt ngôn ngữ và nền tảng khi mở rộng corpus |
| `content_type`, `license_or_permission` | Chuỗi | `authored-summary`, mô tả biên soạn | Nêu rõ loại tài liệu và nguồn gốc nội dung |
| `source_file`, `strategy`, `chunk_index` | Chuỗi, Số nguyên | chuỗi, số nguyên từ 0 | Runner bổ sung để truy lại file và vị trí chunk |


---

## 2. Thiết kế chiến lược (Strategy Design) — Nhóm (15 điểm)

> Mỗi thành viên thử **một chiến lược khác nhau** trên cùng bộ tài liệu; nhóm tổng hợp và so sánh ở đây.

### Phân tích đường cơ sở (Baseline Analysis)

Chạy `ChunkingStrategyComparator().compare()` trên 2-3 tài liệu:

| Tài liệu | Chiến lược (Strategy) | Số lượng Chunk | Độ dài trung bình | Giữ được ngữ cảnh không? |
|-----------|----------|-------------|------------|-------------------|
| `buyer-cancel-order.md` | FixedSizeChunker (`fixed_size`) | 3 | 257.33 | Không giữ tốt ranh giới các mục. Cắt ngang phần "Hãng khác SPX" và "Ngoại lệ SPX". |
| `buyer-cancel-order.md` | SentenceChunker (`by_sentences`) | 3 | 240.33 | Tốt hơn fixed-size nhưng đoạn dài vẫn bị chia nhỏ thành nhiều câu độc lập. |
| `buyer-cancel-order.md` | RecursiveChunker (`recursive`) | 3 | 244.00 | Tôn trọng ngắt đoạn, tốt nhất trong số 3 baseline tích hợp. |
| `buyer-order-status.md` | FixedSizeChunker (`fixed_size`) | 2 | 299.00 | Do văn bản ngắn nên việc cắt không ảnh hưởng nhiều ngữ cảnh. |
| `buyer-order-status.md` | SentenceChunker (`by_sentences`) | 2 | 285.50 | Gom câu khá tốt do thông tin dạng liệt kê. |
| `buyer-order-status.md` | RecursiveChunker (`recursive`) | 3 | 192.67 | Cắt theo dòng (`\n\n`) tạo ra nhiều chunk nhỏ nhưng sạch sẽ. |

### Chiến lược của từng thành viên

> Mỗi thành viên điền một khối dưới đây (copy thêm nếu nhóm có nhiều hơn 3 người).

**Thành viên 1 — Phan Danh Đạt**
- **Loại chiến lược:** HeadingChunker (custom)
- **Mô tả & lý do chọn cho chủ đề này:** Chia văn bản dựa trên các thẻ tiêu đề (Markdown Header `#`, `##`). Với tài liệu chính sách của Shopee, mỗi `##` thường là một điều kiện riêng lẻ (như "Hãng vận chuyển khác SPX" hay "Ngoại lệ SPX"). Việc chia theo tiêu đề giúp bảo toàn trọn vẹn mạch ý của từng trường hợp.
- **Code snippet (nếu custom):**
```python
# Lọc qua các dòng, nếu dòng bắt đầu bằng '#' thì tạo chunk mới.
# Đồng thời ghim lại tiêu đề (heading) vào nội dung của các chunk con bên trong.
def chunk(self, text: str) -> list[str]:
    # (Đã triển khai trong file src/heading_chunking.py)
    pass
```

**Thành viên 2 — Mai Hoàng Anh**
- **Loại chiến lược:** FixedSizeChunker (chunk_size=350, overlap=50)
- **Mô tả & lý do chọn:** Cắt văn bản thành các khối tĩnh với số lượng ký tự cố định, kết hợp chồng chéo (overlap) 50 ký tự. Chiến lược này triển khai đơn giản, giúp hệ thống không bị tràn token context, đồng thời overlap giúp giảm tình trạng thông tin quan trọng bị chặt đứt ở ranh giới hai chunk.

**Thành viên 3 — Hoàng Văn Sơn**
- **Loại chiến lược:** RecursiveChunker (chunk_size=500)
- **Mô tả & lý do chọn:** Chia văn bản đệ quy theo các dấu phân cách (separator) tự nhiên như `\n\n`, `\n`, `. `. Chiến lược này ưu tiên giữ nguyên cấu trúc đoạn văn, chỉ khi đoạn văn quá dài mới chặt ra. Phù hợp cho văn bản dạng hướng dẫn có nhiều gạch đầu dòng dài.

### So Sánh Giữa Các Thành Viên

| Thành viên | Chiến lược (Strategy) | Điểm truy xuất (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| Phan Danh Đạt | HeadingChunker | 10 | Bằng chứng luôn ở hạng 1, không lẫn lộn ngữ cảnh. | Khó triển khai, phụ thuộc chặt chẽ vào Markdown format. |
| Hoàng Văn Sơn | RecursiveChunker | 9 | Cắt đúng đoạn văn tự nhiên, LLM đọc hiểu tốt. | Vẫn bị cắt mất "tiêu đề" dẫn tới LLM bịa tên giao diện. |
| Mai Hoàng Anh | FixedSizeChunker | 8 | Đều đặn, tối ưu tốt cho indexer. | Cắt mù quáng khiến điều kiện (chunk 0) rớt hạng sau ngoại lệ (chunk 1). |

**Chiến lược nào tốt nhất cho chủ đề này? Tại sao?**
> **HeadingChunker** là tốt nhất cho bộ dữ liệu chính sách Shopee. Các tài liệu này được viết dưới dạng cẩm nang có cấu trúc (các trường hợp cụ thể nằm ở từng mục `##`). Việc cắt theo cấu trúc heading giúp mô hình luôn biết đoạn text thuộc "Ngữ cảnh nào, điều kiện nào", từ đó trả lời chính xác mà không bị nhầm lẫn giữa điều kiện chuẩn và ngoại lệ.

---

## 3. Câu hỏi đánh giá & Chất lượng truy xuất (Retrieval Quality) — Nhóm (10 điểm)

### Câu hỏi đánh giá & Câu trả lời chuẩn (nhóm thống nhất)

> **Đúng 5 câu hỏi**, đa dạng, có thể kiểm chứng; **ít nhất 1 câu** cần lọc metadata mới trả lời tốt. Đây là bộ câu hỏi chung cho mọi thành viên chạy.

| # | Câu hỏi (Query) | Câu trả lời chuẩn (Gold Answer) | Chunk nào chứa thông tin? |
|---|-------|-------------------------------|--------------------------|
| 1 | Tôi cần vào đâu trên ứng dụng Shopee để xem trạng thái đơn mua? | Mở mục Tôi > Đơn mua trên ứng dụng Shopee để xem tiến trình đơn hàng. | `buyer-order-status` |
| 2 | Đơn do hãng vận chuyển khác SPX đang Chờ lấy hàng thì tôi có thể hủy ngay không? | Không tự động hủy ngay: phải chờ người bán chấp nhận. Nếu người bán từ chối, đơn vẫn tiếp tục giao. | `buyer-cancel-order` (Lọc: buyer) |
| 3 | Đơn Shopee đã hủy có khôi phục để giao lại và giữ ưu đãi cũ được không? | Không khôi phục đơn đã hủy để giao lại. Cần đặt đơn mới; có thể trao đổi giá với shop, không mặc định giữ được ưu đãi cũ. | `buyer-cancelled-order` |
| 4 | Đơn trả trước bằng thẻ tín dụng hoặc ghi nợ cần thanh toán trong bao lâu, nếu quá hạn thì sao? | Hoàn tất trong 12 giờ kể từ lúc đặt hàng thành công; quá hạn không thanh toán thì hệ thống tự động hủy đơn. | `buyer-prepayment` |
| 5 | Tôi xử lý yêu cầu hủy đơn hàng như thế nào? | Với vai trò người bán trên Kênh Quản Lý Shop: vào Đơn hủy > Chờ phản hồi > Xem thêm, đồng ý hoặc từ chối. | `seller-cancel-request` (Lọc: seller) |

### Tổng hợp chất lượng truy xuất của nhóm

> Cách chấm (theo `docs/SCORING.md`): **2 điểm/câu** — top-3 chứa chunk liên quan + agent trả lời đúng (2), có liên quan nhưng thiếu/không ở top-1 (1), không có trong top-3 (0).

| # | Câu hỏi | Chiến lược tốt nhất cho câu này | Có chunk liên quan trong top-3? | Ghi chú |
|---|---------|-------------------------------|-------------------------------|---------|
| 1 | Tôi cần vào đâu trên ứng dụng... | Cả 3 chiến lược | Cả 3 đều Có | Cả 3 trả lời đúng trọn vẹn nơi xem trạng thái (đều 2 điểm). |
| 2 | Đơn do hãng khác SPX... | HeadingChunker | Cả 3 đều Có | FixedSize bị trích xuất Ngoại lệ SPX lên Top-1 thay vì điều kiện gốc (1 điểm). Heading đẩy bằng chứng lên hạng 1. |
| 3 | Đơn Shopee đã hủy... | Cả 3 chiến lược | Cả 3 đều Có | Đều phân biệt đúng đặt mới với việc khôi phục (2 điểm). |
| 4 | Đơn trả trước... thanh toán bao lâu | Cả 3 chiến lược | Cả 3 đều Có | Trả lời chính xác con số 12 giờ (2 điểm). |
| 5 | Xử lý yêu cầu hủy đơn... | HeadingChunker | Cả 3 đều Có | Recursive & FixedSize đổi tên "Kênh Quản Lý Shop" thành "Kênh Người Bán" trong câu trả lời do mất heading gốc (1 điểm). |

**Lọc bằng metadata có giúp ích không? Ở câu hỏi nào?**
> Rất hữu ích, đặc biệt ở câu số 5. Nếu không lọc `audience=seller`, hệ thống sẽ truy xuất lẫn lộn các quy trình dành cho người mua (buyer) vào top 3. Khi lọc cứng `audience=seller`, kết quả cực kỳ sạch, chỉ giữ lại tài liệu dành cho shop.

---

## 4. Thuyết trình (Demo) & Bài học nhóm — Nhóm (5 điểm)

**Những phân tích (insights) hay nhất nhóm sẽ trình bày:**
- Cùng một bộ dữ liệu, nhưng cắt bằng Fixed-size lại làm đứt điều kiện quan trọng ở Câu 2, khiến mô hình lấy nhầm "Ngoại lệ SPX" xếp hạng 1.
- Mất tiêu đề (Heading) khi dùng Recursive/FixedSize khiến LLM không biết ngữ cảnh nằm ở màn hình nào, dẫn tới tự ảo giác (hallucinate) tên giao diện "Kênh Quản Lý Shop" thành "Kênh Người Bán" (ở Câu 5).

**Bài học rút ra khi so sánh trong nhóm:**
> Chunking là yếu tố quyết định "bằng chứng" mà LLM được nhìn thấy. Dữ liệu tuy chuẩn, mô hình tuy xịn, nhưng nếu chặt văn bản sai chỗ, LLM vẫn sẽ sinh ra câu trả lời thiếu sót hoặc ảo giác.

**Nếu làm lại, nhóm sẽ thay đổi gì trong chiến lược dữ liệu (data strategy)?**
> Nhóm sẽ luôn ép tiêu đề mục (Heading/Section title) vào phần thân của từng đoạn chunk nhỏ (thay vì chỉ cắt dọc). Đồng thời, bổ sung thêm metadata cụ thể hơn như `carrier` (nhà vận chuyển) để không bao giờ bị lẫn lộn giữa SPX và các hãng khác.

---

## Tự Đánh Giá (Phần Nhóm)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Lựa chọn tài liệu (Document Quality) | 10 / 10 |
| Thiết kế chiến lược (Strategy Design) | 15 / 15 |
| Chất lượng truy xuất (Retrieval Quality)| 10 / 10 |
| Thuyết trình (Demo) | 5 / 5 |
| **Tổng phần nhóm** | **40 / 40** |
