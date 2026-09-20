# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Mai Hoàng Anh (MSSV: 2A202602857)
**Nhóm:** G23
**Ngày:** 20/09/2026

> **Nộp 1 bản / sinh viên.** Phần nhóm (lựa chọn tài liệu, thiết kế chiến lược, bộ câu hỏi đánh giá, demo) nộp chung 1 bản trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**
> Hai vector embedding có hướng gần giống nhau, thể hiện rằng ý nghĩa (ngữ nghĩa) của hai đoạn văn bản rất tương đồng dù từ vựng có thể khác nhau.

**Ví dụ có độ tương tự CAO:**
- Câu A: "Tôi muốn hủy đơn hàng này."
- Câu B: "Làm cách nào để xóa bỏ đơn đã đặt?"
- Tại sao tương đồng: Cùng hỏi về mục đích hủy bỏ một đơn hàng vừa mua.

**Ví dụ có độ tương tự THẤP:**
- Câu A: "Tôi muốn hủy đơn hàng này."
- Câu B: "Hôm nay thời tiết thật đẹp."
- Tại sao khác: Hai câu thuộc hai chủ đề hoàn toàn khác nhau (thương mại điện tử vs. thời tiết).

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**
> Cosine similarity chỉ quan tâm đến góc (hướng) giữa 2 vector mà bỏ qua độ lớn (magnitude), giúp so sánh độ tương đồng ngữ nghĩa chính xác hơn bất kể độ dài ngắn của văn bản.

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> *Trình bày phép tính:* Bước nhảy (step) = 500 - 50 = 450. Số lượng chunk = ceil((10000 - 50) / 450) = ceil(9950 / 450) = 23 chunks.
> *Đáp án:* 23 chunks.

**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**
> Số lượng chunk sẽ tăng lên (ceil((10000 - 100) / 400) = 25 chunks). Ta muốn tăng độ chồng chéo để đảm bảo không bị cắt đứt mạch văn, giữ lại được ngữ cảnh (như danh từ riêng, điều kiện) nằm ở ranh giới giữa hai chunk.

---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi lập trình (implement) các phần chính trong gói `src`.

### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:
> Sử dụng thư viện `re` (biểu thức chính quy) để tách văn bản dựa trên các dấu chấm câu kết thúc câu (`. `, `! `, `? `, hoặc `.\n`). Sau đó gom nhóm (join) các câu lại sao cho không vượt quá `max_sentences_per_chunk` và loại bỏ các khoảng trắng thừa.

**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:
> Viết hàm đệ quy `_split`. Nếu đoạn hiện tại dài hơn `chunk_size`, thuật toán thử cắt bằng dấu phân cách (separator) đầu tiên trong danh sách (như `\n\n`). Nếu sau khi cắt và gom lại, có những đoạn vẫn vượt `chunk_size`, thuật toán sẽ đệ quy gọi lại chính nó với mảng dấu phân cách tiếp theo (như `\n`, `.`). Base case là khi đoạn văn nhỏ hơn `chunk_size` hoặc hết separator.

### Lớp EmbeddingStore

**`add_documents` + `search`** — hướng tiếp cận:
> Lưu trữ văn bản và embedding dưới dạng danh sách các đối tượng `Document`. Khi search, dùng hàm `compute_similarity` để tính tích vô hướng (dot product) chia cho tích độ dài chuẩn (L2 norm) giữa vector câu hỏi và từng document, sau đó sắp xếp giảm dần để trả về top K.

**`search_with_filter` + `delete_document`** — hướng tiếp cận:
> Lọc (filter) danh sách document trước khi tính độ tương tự. Chỉ những document có metadata khớp hoàn toàn với `metadata_filter` mới được tính toán, giúp tối ưu hiệu suất. `delete_document` sử dụng list comprehension để lọc bỏ document có ID trùng khớp.

### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:
> Gọi `store.search` (có filter nếu cần) để lấy ra top chunk liên quan nhất. Sau đó ghép nội dung các chunk này thành một chuỗi `context` và truyền vào prompt template dạng: "Dựa vào ngữ cảnh sau: {context}. Hãy trả lời câu hỏi: {query}". Cuối cùng gửi prompt này cho LLM.

---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```text
============================= test session starts =============================
platform win32 -- Python 3.10.0, pytest-8.0.0
collected 42 items

tests/test_solution.py::test_sentence_chunker PASSED                     [  2%]
tests/test_solution.py::test_recursive_chunker PASSED                    [  5%]
tests/test_solution.py::test_similarity PASSED                           [  8%]
tests/test_solution.py::test_embedding_store PASSED                      [ 11%]
tests/test_solution.py::test_agent_rag PASSED                            [ 14%]
...
tests/test_solution.py::test_all_features_integrated PASSED              [100%]

============================= 42 passed in 1.25s ==============================
```

**Số lượng bài test vượt qua (pass):** 42 / 42

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | "Cách hủy đơn hàng Shopee" | "Hướng dẫn xóa đơn đã đặt" | cao | 0.82 | Có |
| 2 | "Đơn hàng đang giao" | "Sản phẩm đã được vận chuyển" | cao | 0.78 | Có |
| 3 | "Tôi muốn đổi trả hàng" | "Cách thanh toán tiền điện" | thấp | 0.15 | Có |
| 4 | "Shop chưa xác nhận đơn" | "Người bán chậm chuẩn bị hàng" | cao | 0.85 | Có |
| 5 | "Thời gian giao hàng là bao lâu?" | "Phí vận chuyển hết bao nhiêu?" | thấp | 0.35 | Có |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
> Cặp 1 và 2 dù không có bất kỳ từ vựng nào trùng lặp ("hủy" vs "xóa", "giao" vs "vận chuyển") nhưng điểm vẫn rất cao. Điều này chứng tỏ embedding mô hình hóa được sự tương đồng về mặt ngữ nghĩa (semantic) chứ không chỉ đối chiếu từ khóa (keyword).

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên mã nguồn cá nhân của bạn (sử dụng **FixedSizeChunker(chunk_size=350, overlap=50)**). 

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | Tôi cần vào đâu trên ứng dụng Shopee để xem trạng thái đơn mua? | `buyer-order-status.md` (chunk 0): Mở Tôi > Đơn mua... | 0.875 | Có | Mở mục Tôi > Đơn mua trên ứng dụng để xem tiến trình. |
| 2 | Đơn do hãng vận chuyển khác SPX đang Chờ lấy hàng thì tôi có thể hủy ngay không? | `buyer-cancel-order.md` (chunk 1): Ngoại lệ SPX Express... | 0.850 | Một phần (Bằng chứng chính nằm ở Top-2) | Agent vẫn trả lời đúng: Phải đợi người bán chấp nhận do ghép ngữ cảnh từ Top-2. |
| 3 | Đơn Shopee đã hủy có khôi phục để giao lại và giữ ưu đãi cũ được không? | `buyer-cancelled-order.md` (chunk 0): Đơn đã hủy và khôi phục... | 0.880 | Có | Không khôi phục được; phải đặt đơn mới, không mặc định giữ ưu đãi. |
| 4 | Đơn trả trước bằng thẻ tín dụng cần thanh toán trong bao lâu? | `buyer-prepayment.md` (chunk 0): Thời hạn thanh toán... | 0.895 | Có | Hoàn tất trong 12 giờ kể từ lúc đặt hàng thành công. |
| 5 | Tôi xử lý yêu cầu hủy đơn hàng như thế nào? (Lọc seller) | `seller-cancel-request.md` (chunk 0): Vào Đơn hủy > Chờ phản hồi... | 0.766 | Có | Vào Kênh Người Bán > Đơn hủy > Chờ phản hồi... (Bị đổi tên từ Kênh Quản Lý Shop). |

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** 5 / 5

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**
> Nhờ so sánh kết quả Fixed-size của tôi với HeadingChunker của Đạt, tôi thấy rõ việc dùng FixedSize có thể khiến điều kiện (ở câu 2) bị tách sang chunk thứ 2, khiến chunk ngoại lệ lại leo lên Top-1. Chunker dựa trên cấu trúc (Heading) bảo toàn mạch ý tốt hơn nhiều.

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | 5 / 5 |
| Hướng tiếp cận của tôi (My Approach) | 10 / 10 |
| Hoàn thiện code (Core Implementation — tests) | 30 / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | 5 / 5 |
| Kết quả truy xuất của tôi (Competition Results) | 10 / 10 |
| **Tổng phần cá nhân** | **60 / 60** |
