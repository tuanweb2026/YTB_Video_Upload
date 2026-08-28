#!/usr/bin/env python3
"""
Tạo 50 Short + 200 bài Video Dài từ kho Kinh Nikaya
Mục tiêu: 1 triệu view trong 2 tháng cho kênh @1995lido
"""
import json, os

SCRATCH_DIR = "/Users/abc/.gemini/antigravity/scratch/1995lido_youtube_management"

# ==========================================
# 50 KỊCH BẢN SHORT VIDEO (60 giây)
# ==========================================
shorts_60 = [
  # --- NHÓM 1: TỨ DIỆU ĐẾ & BÁT CHÁNH ĐẠO (index 11-20) ---
  {
    "index": 11,
    "source_title": "Tứ Diệu Đế - Chân Lý Đầu Tiên: Khổ Đế",
    "title": "Vì Sao Cuộc Đời Có Khổ? Phật Dạy Sự Thật Không Ai Chịu Nhìn Nhận #Shorts #NikayaKinh",
    "hook": "Bạn có bao giờ tự hỏi tại sao dù có đủ mọi thứ nhưng vẫn cảm thấy thiếu vắng và không an lành?",
    "script": "Chào bạn nhen! Đức Phật dạy Khổ Đế - sự thật đầu tiên trong Tứ Diệu Đế: Cuộc đời có bản chất là khổ. Sinh là khổ, già là khổ, bệnh là khổ, chết là khổ. Không phải để bi quan, mà để tỉnh thức. Hiểu rõ khổ, bạn mới không chạy trốn nó mà đối diện và vượt qua. Đây là bước đầu tiên trên con đường giải thoát nhen! Nhấn Đăng Ký Kênh Thảo Dương TV để cùng học triết lý chánh kiến mỗi ngày nhen!",
    "category": "Triết Lý Nikaya - Tứ Diệu Đế",
    "tags": ["NikayaKinh","ThảoDươngTV","TứDiệuĐế","KhổĐế","Shorts"]
  },
  {
    "index": 12,
    "source_title": "Tập Đế - Nguyên Nhân Của Khổ",
    "title": "Gốc Rễ Của Mọi Đau Khổ Là Gì? Phật Tiết Lộ Điều Bạn Không Ngờ Tới #Shorts #NikayaKinh",
    "hook": "Nếu bệnh mà không biết nguyên nhân, bác sĩ không thể chữa trị. Khổ đau cũng vậy...",
    "script": "Dạ chào bạn nhen! Tập Đế - chân lý thứ hai: Khổ đau sinh ra từ Tham - Sân - Si. Tham muốn quá nhiều, ghét bỏ những điều không vừa ý, và si mê không nhìn thấy bản chất thật của sự vật. Ba độc này là ngọn lửa âm ỉ đốt cháy tâm ta từng ngày. Nhận ra chúng là bước đầu để tắt lửa khổ đau nhen! Bấm Đăng Ký Kênh Thảo Dương TV để được học thêm nhen!",
    "category": "Triết Lý Nikaya - Tứ Diệu Đế",
    "tags": ["NikayaKinh","ThảoDươngTV","TậpĐế","TamĐộc","Shorts"]
  },
  {
    "index": 13,
    "source_title": "Diệt Đế - Trạng Thái Niết Bàn",
    "title": "Niết Bàn Là Gì? Không Phải Chết - Mà Là Đỉnh Cao Hạnh Phúc Thật Sự #Shorts #NikayaKinh",
    "hook": "Nhiều người nghĩ Niết Bàn là chết đi. Thực ra đó là trạng thái hạnh phúc viên mãn nhất...",
    "script": "Chào bạn nhen! Diệt Đế - chân lý thứ ba: Khổ đau hoàn toàn có thể chấm dứt. Niết Bàn không phải là hư vô hay cái chết. Đó là trạng thái tâm hoàn toàn tự do - không còn Tham, Sân, Si đốt cháy. Giống như ngọn lửa tắt khi hết củi, khổ đau tắt khi ta hết tham ái. Đây là mục tiêu tối thượng của con đường tu tập nhen! Đăng Ký Kênh Thảo Dương TV để đi trên con đường đó cùng nhau nhen!",
    "category": "Triết Lý Nikaya - Tứ Diệu Đế",
    "tags": ["NikayaKinh","ThảoDươngTV","DiệtĐế","NiếtBàn","Shorts"]
  },
  {
    "index": 14,
    "source_title": "Đạo Đế - Bát Chánh Đạo",
    "title": "8 Bước Thoát Khỏi Khổ Đau - Con Đường Mà Phật Đã Đi #Shorts #NikayaKinh",
    "hook": "Có con đường 8 bước dẫn đến hạnh phúc thật sự - không phải tiền bạc, danh vọng...",
    "script": "Dạ chào bạn nhen! Bát Chánh Đạo - con đường thoát khổ gồm 8 yếu tố: Chánh Kiến, Chánh Tư Duy, Chánh Ngữ, Chánh Nghiệp, Chánh Mạng, Chánh Tinh Tấn, Chánh Niệm, Chánh Định. Đây là con đường trung đạo - không quá khắc khổ, không quá dễ dãi. Mỗi ngày thực hành từng chút một, tâm ta dần trong sáng và an lạc hơn nhen! Nhấn Đăng Ký Kênh Thảo Dương TV để cùng bước trên con đường này nhen!",
    "category": "Triết Lý Nikaya - Bát Chánh Đạo",
    "tags": ["NikayaKinh","ThảoDươngTV","BátChánh Đạo","ConĐườngThoátKhổ","Shorts"]
  },
  {
    "index": 15,
    "source_title": "Chánh Kiến - Hiểu Đúng Bản Chất Thực Tại",
    "title": "Nhìn Đời Không Méo Mó: Bí Quyết Tư Duy Chánh Kiến Của Người Trí Tuệ #Shorts #NikayaKinh",
    "hook": "Nếu kính có vết nứt, mọi thứ bạn nhìn đều bị méo mó. Tâm trí cũng vậy...",
    "script": "Chào bạn nhen! Chánh Kiến là yếu tố đầu tiên của Bát Chánh Đạo - thấy mọi thứ đúng như bản chất thật của nó: Vô thường, Khổ, Vô ngã. Không lãng mạn hóa quá mức, không bi quan méo mó. Khi nhìn đời với Chánh Kiến, bạn không bị ảo tưởng hay thất vọng dẫn dắt. Bạn sống tỉnh thức và làm chủ phản ứng của mình nhen! Đăng Ký Kênh Thảo Dương TV để rèn Chánh Kiến mỗi ngày nhen!",
    "category": "Triết Lý Nikaya - Bát Chánh Đạo",
    "tags": ["NikayaKinh","ThảoDươngTV","CháinhKiến","TưDuyĐúng","Shorts"]
  },
  # --- NHÓM 2: TAM HỌC - GIỚI ĐỊNH TUỆ (index 16-20) ---
  {
    "index": 16,
    "source_title": "Giới Học - Nền Tảng Đạo Đức Phật Giáo",
    "title": "Ngũ Giới Là Gì? 5 Lời Hứa Với Bản Thân Để Sống Không Hối Tiếc #Shorts #NikayaKinh",
    "hook": "5 điều này không phải luật cấm đoán - mà là món quà bạn tặng cho chính mình...",
    "script": "Dạ chào bạn nhen! Ngũ Giới trong Nikaya là 5 nền tảng đạo đức: Không sát sinh, Không trộm cắp, Không tà dâm, Không nói dối, Không uống rượu. Mỗi giới này không phải hình phạt - mà là sự bảo vệ. Không gây hại người khác nghĩa là bảo vệ tâm ta khỏi cảm giác tội lỗi và sợ hãi. Sống đúng Ngũ Giới là sống trong sạch và nhẹ lòng nhất nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!",
    "category": "Triết Lý Nikaya - Tam Học Giới",
    "tags": ["NikayaKinh","ThảoDươngTV","NgũGiới","ĐạoĐức","Shorts"]
  },
  {
    "index": 17,
    "source_title": "Định Học - Sức Mạnh Của Tâm Thiền Định",
    "title": "Thiền Định Không Phải Ngồi Bất Động - Đây Là Sức Mạnh Thật Sự Của Nó #Shorts #NikayaKinh",
    "hook": "Thiền định không phải là trốn chạy thực tại - mà là đối diện trực tiếp với tâm mình...",
    "script": "Chào bạn nhen! Định Học trong Nikaya dạy ta phát triển 4 tầng thiền định Jhana. Từ tầng 1 - tâm trí bình lặng, đến tầng 4 - trạng thái xả niệm thanh tịnh thuần túy. Mỗi ngày chỉ cần 10-15 phút ngồi yên, theo dõi hơi thở, không phán xét. Não bạn sẽ dần bình tĩnh hơn, sáng suốt hơn trong mọi quyết định của cuộc sống nhen! Đăng Ký Kênh Thảo Dương TV để học thiền đúng cách nhen!",
    "category": "Triết Lý Nikaya - Tam Học Định",
    "tags": ["NikayaKinh","ThảoDươngTV","ThiềnĐịnh","TâmBìnhLặng","Shorts"]
  },
  {
    "index": 18,
    "source_title": "Tuệ Học - Trí Tuệ Giải Thoát",
    "title": "Trí Tuệ Phật Giáo Khác Gì Với Thông Minh Thông Thường? Đây Là Câu Trả Lời #Shorts #NikayaKinh",
    "hook": "IQ cao chưa chắc hạnh phúc. Trí tuệ Bát Nhã mới là loại khôn ngoan thật sự...",
    "script": "Dạ chào bạn nhen! Tuệ học trong Nikaya là trí tuệ thấy rõ Tam Pháp Ấn: Vô thường, Khổ, Vô ngã. Người thông minh biết nhiều thông tin. Người có Tuệ biết bản chất thực của sự vật. Khi thấy rõ mọi thứ đều vô thường, ta không còn bám chặt vào nó và đau khổ khi mất đi. Tuệ học là đỉnh cao của Tam Học Giới-Định-Tuệ nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!",
    "category": "Triết Lý Nikaya - Tam Học Tuệ",
    "tags": ["NikayaKinh","ThảoDươngTV","TuệHọc","TríTuệGiảiThoát","Shorts"]
  },
  {
    "index": 19,
    "source_title": "Ba Đặc Tính Của Hiện Tượng - Tam Pháp Ấn",
    "title": "3 Sự Thật Về Cuộc Đời Mà Phật Dạy - Hiểu Rồi Bạn Không Còn Sợ Nữa #Shorts #NikayaKinh",
    "hook": "Có 3 sự thật mà khi hiểu rõ, bạn sẽ không bao giờ đau khổ vì bất cứ điều gì nữa...",
    "script": "Chào bạn nhen! Ba Pháp Ấn hay Tam Tướng trong Nikaya: Vô Thường (Anicca) - mọi thứ đều thay đổi, Khổ (Dukkha) - không thứ gì mang lại hạnh phúc hoàn toàn bền vững, Vô Ngã (Anatta) - không có cái tôi cố định bất biến. Hiểu 3 điều này không phải để bi quan mà để buông bỏ đúng cách và sống tự do hơn mỗi ngày nhen! Nhấn Đăng Ký Kênh Thảo Dương TV nhen!",
    "category": "Triết Lý Nikaya - Tam Pháp Ấn",
    "tags": ["NikayaKinh","ThảoDươngTV","TamPháp Ấn","VôThường","Shorts"]
  },
  {
    "index": 20,
    "source_title": "Lý Duyên Khởi - Mọi Thứ Đều Tương Quan",
    "title": "Tại Sao Không Ai Có Thể Sống Độc Lập Hoàn Toàn? Phật Dạy Điều Kỳ Diệu Này #Shorts #NikayaKinh",
    "hook": "Một bông hoa cần đất, nước, ánh sáng, người trồng... Mọi thứ đều kết nối với nhau...",
    "script": "Dạ chào bạn nhen! Lý Duyên Khởi (Paticca-samuppada) trong Nikaya dạy rằng mọi hiện tượng đều phát sinh do nhiều điều kiện hỗ trợ nhau. Không có gì tồn tại độc lập. Khi hiểu điều này, ta trân trọng hơn mối quan hệ với người khác, với thiên nhiên. Tâm ta bớt ích kỷ và mở ra với sự kết nối rộng lớn hơn. Đây là nền tảng của lòng từ bi nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!",
    "category": "Triết Lý Nikaya - Duyên Khởi",
    "tags": ["NikayaKinh","ThảoDươngTV","DuyênKhởi","TươngQuan","Shorts"]
  },
  # --- NHÓM 3: TÂM LÝ VÀ CẢM XÚC HIỆN ĐẠI (index 21-35) ---
  {
    "index": 21,
    "source_title": "Kinh Kalama - Hướng Dẫn Tư Duy Phản Biện",
    "title": "Phật Dạy: Đừng Tin Vì Nghe Nói - Hãy Tự Kiểm Chứng Bằng Trải Nghiệm #Shorts #NikayaKinh",
    "hook": "2600 năm trước Phật đã dạy tư duy phản biện. Điều đó cần thiết hơn bao giờ hết trong thời đại mạng xã hội...",
    "script": "Chào bạn nhen! Kinh Kalama nổi tiếng nhất trong Nikaya: Đức Phật dạy đừng tin chỉ vì đọc sách, vì truyền thống, vì thầy dạy, vì đa số tin. Hãy tự mình kiểm nghiệm: Điều này khi thực hành có dẫn đến lợi ích thật sự không? Có giảm khổ đau không? Đây là tinh thần khoa học, tư duy độc lập - hiếm có tôn giáo nào dạy điều này nhen! Đăng Ký Kênh Thảo Dương TV nhen!",
    "category": "Triết Lý Nikaya - Tư Duy Độc Lập",
    "tags": ["NikayaKinh","ThảoDươngTV","TưDuyPhảnBiện","KinhKalama","Shorts"]
  },
  {
    "index": 22,
    "source_title": "Cách Xử Lý Cơn Giận Theo Phật Dạy",
    "title": "Khi Muốn Nổi Giận - Hãy Làm Đúng 1 Điều Này Theo Lời Phật Dạy #Shorts #NikayaKinh",
    "hook": "Giận 1 giây có thể phá hủy 10 năm quan hệ. Phật có cách xử lý khác hoàn toàn...",
    "script": "Dạ chào bạn nhen! Trong Tương Ưng Bộ Kinh, Phật dạy: Khi cơn giận nổi lên, hãy nhìn nó như đám lửa đang bùng cháy trong tâm. Không thêm củi bằng lời nói. Không dập bằng cách đè nén. Chỉ quan sát nó đang thay đổi và tự tắt. Cơn giận có tuổi thọ ngắn lắm - chỉ 90 giây - nếu bạn không nuôi dưỡng nó bằng suy nghĩ thêm nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!",
    "category": "Triết Lý Nikaya - Xử Lý Cơn Giận",
    "tags": ["NikayaKinh","ThảoDươngTV","XửLýGiận","CháinhNiệm","Shorts"]
  },
  {
    "index": 23,
    "source_title": "Kinh Sợ Hãi & Lo Âu Theo Phật Dạy",
    "title": "Phật Dạy Cách Vượt Qua Nỗi Sợ Hãi Mà Không Cần Thuốc Hay Liệu Pháp #Shorts #NikayaKinh",
    "hook": "Nỗi sợ thường không phải về điều đang xảy ra - mà là về điều bạn tưởng tượng sẽ xảy ra...",
    "script": "Chào bạn nhen! Trong Trung Bộ Kinh, Phật dạy: Sợ hãi xuất phát từ tham ái và vô minh. Ta sợ vì muốn giữ những thứ vô thường và không biết bản chất thật của sự vật. Liều thuốc là Chánh Niệm - quan sát nỗi sợ không phán xét. Hỏi: Điều tôi sợ có đang xảy ra ngay lúc này không? Phần lớn nỗi sợ sống trong tương lai tưởng tượng, không phải hiện tại nhen! Đăng Ký Kênh Thảo Dương TV nhen!",
    "category": "Triết Lý Nikaya - Vượt Qua Sợ Hãi",
    "tags": ["NikayaKinh","ThảoDươngTV","VượtQuaSợHãi","CháinhNiệm","Shorts"]
  },
  {
    "index": 24,
    "source_title": "Lòng Biết Ơn Theo Phật Dạy",
    "title": "Tại Sao Biết Ơn Là Thực Hành Quan Trọng Nhất Trong Phật Giáo? #Shorts #NikayaKinh",
    "hook": "Người không biết ơn sẽ không bao giờ thật sự hạnh phúc dù có bao nhiêu đi nữa...",
    "script": "Dạ chào bạn nhen! Phật dạy trong Tăng Chi Bộ: Người biết ơn (Katannu) là người trí tuệ. Lòng biết ơn mở ra tâm hoan hỷ, ngăn Tham Sân Si phát sinh. Mỗi buổi sáng, trước khi bước ra khỏi giường, hãy nghĩ đến 3 điều bạn đang biết ơn: hơi thở, sức khỏe, người thân... Thực hành này thay đổi não bộ và cảm xúc trong vài tuần nhen! Bấm Đăng Ký Kênh Thảo Dương TV nhen!",
    "category": "Triết Lý Nikaya - Lòng Biết Ơn",
    "tags": ["NikayaKinh","ThảoDươngTV","BiếtƠn","HoanHỷ","Shorts"]
  },
  {
    "index": 25,
    "source_title": "Nghệ Thuật Buông Bỏ - Không Phải Từ Bỏ",
    "title": "Buông Bỏ Không Phải Là Yếu Đuối - Đây Là Sức Mạnh Thật Sự #Shorts #NikayaKinh",
    "hook": "Người ta nhầm lẫn buông bỏ với từ bỏ. Nhưng đó là hai thứ hoàn toàn khác nhau...",
    "script": "Chào bạn nhen! Phật dạy Upadana - sự bám chấp là nguồn gốc khổ đau. Buông bỏ (Vossagga) không phải là thụ động hay từ bỏ trách nhiệm. Đó là làm hết sức mình rồi không bám vào kết quả. Như người nông dân cày xới, gieo hạt, tưới nước - nhưng không kiểm soát được mưa nắng. Làm tốt phần của mình, kết quả để tự nhiên nhen! Đăng Ký Kênh Thảo Dương TV để học nghệ thuật này nhen!",
    "category": "Triết Lý Nikaya - Nghệ Thuật Buông Bỏ",
    "tags": ["NikayaKinh","ThảoDươngTV","BuôngBỏ","KhôngBámChấp","Shorts"]
  },
  {
    "index": 26,
    "source_title": "Tứ Vô Lượng Tâm - Từ Bi Hỷ Xả",
    "title": "4 Loại Tình Yêu Thương Cao Nhất Mà Phật Dạy - Bạn Đang Ở Mức Nào? #Shorts #NikayaKinh",
    "hook": "Tình yêu có 4 tầng. Hầu hết chúng ta chỉ biết tầng 1. Hãy học 3 tầng còn lại...",
    "script": "Dạ chào bạn nhen! Tứ Vô Lượng Tâm trong Nikaya: Từ (Metta) - mong người được hạnh phúc, Bi (Karuna) - mong người thoát khổ, Hỷ (Mudita) - vui khi người khác được vui, Xả (Upekkha) - bình đẳng không phân biệt. Luyện tập 4 tâm này mỗi ngày, ta trở nên rộng lượng hơn, bớt ganh tỵ và sân hận. Đây là công thức xây dựng mối quan hệ lành mạnh nhen! Bấm Đăng Ký nhen!",
    "category": "Triết Lý Nikaya - Tứ Vô Lượng Tâm",
    "tags": ["NikayaKinh","ThảoDươngTV","TứVôLượngTâm","TừBiHỷXả","Shorts"]
  },
  {
    "index": 27,
    "source_title": "Trung Đạo - Con Đường Cân Bằng",
    "title": "Bí Quyết Sống Cân Bằng Của Phật - Không Quá Nghiêm Khắc Cũng Không Quá Buông Thả #Shorts",
    "hook": "Đàn violin lên dây quá căng sẽ đứt. Quá lỏng sẽ không kêu. Cuộc sống cũng cần trung đạo...",
    "script": "Chào bạn nhen! Trung Đạo (Majjhima Patipada) là một trong những khám phá quan trọng nhất của Đức Phật. Trước khi giác ngộ, Ngài đã thử sống cực kỳ xa hoa và cực kỳ khổ hạnh - cả hai đều không dẫn đến giải thoát. Con đường ở giữa: Kỷ luật mà không hành hạ. Buông bỏ mà không từ bỏ trách nhiệm. Nỗ lực mà không căng thẳng. Đây là chìa khóa sống lành mạnh nhen! Đăng Ký Kênh nhen!",
    "category": "Triết Lý Nikaya - Trung Đạo",
    "tags": ["NikayaKinh","ThảoDươngTV","TrungĐạo","CânBằng","Shorts"]
  },
  {
    "index": 28,
    "source_title": "Ái Ngữ - Ngôn Ngữ Của Tình Thương",
    "title": "Nói Chuyện Như Phật Dạy: 5 Tiêu Chí Để Lời Nói Chữa Lành Thay Vì Gây Tổn Thương #Shorts",
    "hook": "Lời nói có thể là thuốc chữa lành hoặc con dao đâm vào tim người khác. Phật dạy cách chọn...",
    "script": "Dạ chào bạn nhen! Trong Trường Bộ Kinh, Phật dạy 5 tiêu chí của Ái Ngữ: Đúng sự thật, Ôn hòa không thô ác, Có lợi ích cho người nghe, Nói đúng lúc đúng chỗ, Xuất phát từ lòng từ bi. Trước khi nói, hãy tự hỏi 3 câu: Điều này đúng không? Điều này cần thiết không? Điều này sẽ giúp ích không? Nếu cả 3 đều không thì giữ im lặng là thượng sách nhen! Bấm Đăng Ký nhen!",
    "category": "Triết Lý Nikaya - Ái Ngữ",
    "tags": ["NikayaKinh","ThảoDươngTV","ÁiNgữ","LờiNóiChữaLành","Shorts"]
  },
  {
    "index": 29,
    "source_title": "Kiên Nhẫn Và Sức Chịu Đựng Theo Phật Dạy",
    "title": "Khantī - Nhẫn Nhục Phật Dạy Khác Hoàn Toàn Với Cam Chịu Thụ Động #Shorts #NikayaKinh",
    "hook": "Nhẫn nhục không phải nuốt cay đắng vào trong. Đó là sức mạnh thầm lặng của người trí tuệ...",
    "script": "Chào bạn nhen! Khantī - Nhẫn nhục trong Nikaya là một trong 10 Pāramī (hạnh ba la mật). Đây không phải là thụ động hay cam chịu. Đó là sức mạnh giữ tâm bình thản trước nghịch cảnh trong khi vẫn hành động chánh đáng. Như cây dẻo dai cúi xuống trước bão mà không gãy. Nhẫn nhục thật sự cần nhiều nội lực hơn nổi giận rất nhiều nhen! Đăng Ký Kênh Thảo Dương TV nhen!",
    "category": "Triết Lý Nikaya - Nhẫn Nhục",
    "tags": ["NikayaKinh","ThảoDươngTV","NhẫnNhục","NộiLực","Shorts"]
  },
  {
    "index": 30,
    "source_title": "Sống Tỉnh Thức Trong Từng Khoảnh Khắc",
    "title": "Bạn Đang Sống Hay Chỉ Đang Tồn Tại? Phật Dạy Sự Khác Biệt Quan Trọng Này #Shorts",
    "hook": "85% thời gian, tâm trí ta đang ở một nơi khác hoàn toàn, không phải nơi cơ thể đang đứng...",
    "script": "Dạ chào bạn nhen! Nghiên cứu Harvard phát hiện tâm trí con người lạc đề 47% thời gian thức. Phật dạy điều này 2600 năm trước và gọi là Sampajañña - tỉnh giác rõ ràng. Thực hành đơn giản: Khi ăn chỉ ăn, khi đi chỉ đi, khi nghe chỉ nghe. Không vừa ăn vừa xem điện thoại. Hiện diện 100% trong khoảnh khắc này là món quà lớn nhất bạn có thể tặng cho mình nhen! Bấm Đăng Ký nhen!",
    "category": "Triết Lý Nikaya - Sống Tỉnh Thức",
    "tags": ["NikayaKinh","ThảoDươngTV","SốngTỉnhThức","Mindfulness","Shorts"]
  },
  {
    "index": 31,
    "source_title": "Năm Triền Cái - Chướng Ngại Tâm Lý",
    "title": "5 Thứ Này Đang Làm Nghẹt Thở Tâm Trí Bạn Mà Bạn Không Hề Hay Biết #Shorts #NikayaKinh",
    "hook": "Giống như 5 loại cỏ dại bóp nghẹt cây trồng, có 5 thứ đang làm mờ đi trí tuệ của bạn...",
    "script": "Chào bạn nhen! Năm Triền Cái trong Nikaya là 5 chướng ngại tâm lý: Tham dục, Sân hận, Hôn trầm thụy miên (buồn ngủ, uể oải), Trạo cử hối quá (bồn chồn, lo lắng), Hoài nghi. Khi 5 cái này kéo đến, tâm ta như nước đục - không thể nhìn thấy rõ ràng. Nhận biết được chúng là bước đầu để tạm thời gạt chúng sang bên và tìm lại sự sáng suốt nhen! Đăng Ký Kênh nhen!",
    "category": "Triết Lý Nikaya - Năm Triền Cái",
    "tags": ["NikayaKinh","ThảoDươngTV","NămTriềnCái","TâmLý","Shorts"]
  },
  {
    "index": 32,
    "source_title": "Thiện Tri Thức - Tầm Quan Trọng Của Bạn Bè Tốt",
    "title": "Phật Dạy: Bạn Bè Tốt Là Toàn Bộ Của Con Đường Tu Tập - Không Phải Phân Nửa #Shorts",
    "hook": "Người ta thường nói bạn bè tốt là nửa con đường. Phật nói: Không, đó là toàn bộ con đường...",
    "script": "Dạ chào bạn nhen! Trong Tương Ưng Bộ, Ananda hỏi Phật: Thiện tri thức (bạn đạo tốt) có phải là phân nửa phạm hạnh không? Phật đáp: Không, Ananda! Thiện tri thức là toàn bộ phạm hạnh. Người có bạn tốt sẽ dễ tu tập và giác ngộ hơn rất nhiều. Hãy cẩn thận chọn lựa ai bạn dành thời gian cho - họ ảnh hưởng đến tâm và hành vi của bạn sâu sắc nhất nhen! Bấm Đăng Ký nhen!",
    "category": "Triết Lý Nikaya - Thiện Tri Thức",
    "tags": ["NikayaKinh","ThảoDươngTV","BạnBèTốt","ThiệnTriThức","Shorts"]
  },
  {
    "index": 33,
    "source_title": "Vô Ngã - Không Có Cái Tôi Cố Định",
    "title": "Nếu Không Có Cái Tôi Cố Định Thì Ai Đang Đọc Những Dòng Này? Phật Giải Thích #Shorts",
    "hook": "Câu hỏi này làm nhiều triết gia điên đầu suốt ngàn năm. Phật có câu trả lời đơn giản hơn...",
    "script": "Chào bạn nhen! Vô Ngã (Anatta) trong Nikaya: Không có cái tôi bất biến, cố định. Thứ mà bạn gọi là 'tôi' thực ra là sự tập hợp tạm thời của 5 Uẩn: Sắc (thân), Thọ (cảm giác), Tưởng (nhận thức), Hành (ý chí), Thức (ý thức). Chúng liên tục thay đổi. Người 20 tuổi và 60 tuổi không phải cùng một người. Hiểu Vô Ngã giúp ta bớt tự ái và cởi mở hơn với sự thay đổi nhen! Đăng Ký nhen!",
    "category": "Triết Lý Nikaya - Vô Ngã",
    "tags": ["NikayaKinh","ThảoDươngTV","VôNgã","Anatta","Shorts"]
  },
  {
    "index": 34,
    "source_title": "Hạnh Phúc Bền Vững Theo Phật Dạy",
    "title": "Hạnh Phúc Mà Tiền Không Mua Được - Phật Dạy Cách Tìm Thứ Đó #Shorts #NikayaKinh",
    "hook": "Nghiên cứu Harvard kéo dài 80 năm chứng minh điều Phật dạy 2600 năm trước về hạnh phúc...",
    "script": "Dạ chào bạn nhen! Phật phân biệt 2 loại hạnh phúc: Hỷ lạc tạm thời từ dục vọng (nhanh đến, nhanh đi) và Tịnh lạc bền vững từ nội tâm thanh thản. Giảng Harvard về hạnh phúc 80 năm cũng kết luận: Không phải tiền hay địa vị, mà chất lượng mối quan hệ và sự bình an nội tâm mới tạo hạnh phúc dài lâu. Phật dạy điều này từ thế kỷ 5 trước Công Nguyên nhen! Bấm Đăng Ký nhen!",
    "category": "Triết Lý Nikaya - Hạnh Phúc Bền Vững",
    "tags": ["NikayaKinh","ThảoDươngTV","HạnhPhúcThậtSự","NộiTâm","Shorts"]
  },
  {
    "index": 35,
    "source_title": "Tỉnh Thức Khi Đối Mặt Với Chỉ Trích",
    "title": "Phật Dạy Cách Xử Lý Lời Phê Bình Mà Không Bị Tổn Thương Hay Kiêu Ngạo #Shorts",
    "hook": "Khi bị chỉ trích bạn phản ứng thế nào? Phật có một thí dụ rất hay về điều này...",
    "script": "Chào bạn nhen! Trong Udana, có người đến chửi mắng Phật thậm tệ. Phật hỏi: Nếu bạn tặng quà mà người kia không nhận thì quà đó thuộc về ai? Người đó nói: Của tôi. Phật đáp: Lời chửi của bạn tôi không nhận. Nó vẫn thuộc về bạn. Chúng ta không thể kiểm soát lời người khác nói, nhưng hoàn toàn có thể kiểm soát việc mình có nhận nó vào tâm hay không nhen! Đăng Ký Kênh nhen!",
    "category": "Triết Lý Nikaya - Đối Mặt Phê Bình",
    "tags": ["NikayaKinh","ThảoDươngTV","ĐốiMặtChỉTrích","TâmBìnhTĩnh","Shorts"]
  },
  # --- NHÓM 4: TÀI CHÍNH VÀ NGHỀ NGHIỆP THEO PHẬT DẠY (index 36-45) ---
  {
    "index": 36,
    "source_title": "Kinh Dighajanu - Hạnh Phúc Thế Tục Theo Phật Dạy",
    "title": "Phật Không Chỉ Dạy Xuất Gia - Đây Là Lời Khuyên Tài Chính Cho Người Thế Tục #Shorts",
    "hook": "Nhiều người nghĩ Phật giáo chỉ cho nhà sư. Nhưng Phật có cả hướng dẫn cụ thể cho người làm ăn...",
    "script": "Dạ chào bạn nhen! Trong Kinh Dighajanu, Phật dạy người thế tục 4 bí quyết hạnh phúc vật chất: 1 - Siêng năng có kỹ năng trong nghề. 2 - Bảo vệ thu nhập, tiết kiệm thông minh. 3 - Kết bạn với người tốt, tránh xa kẻ xấu. 4 - Mưu sinh cân bằng - không quá tiện tặn cũng không phung phí. Phật không chỉ dạy thiền định - ngài cũng dạy cách làm ăn thịnh vượng nhen! Bấm Đăng Ký nhen!",
    "category": "Triết Lý Nikaya - Tài Chính Thế Tục",
    "tags": ["NikayaKinh","ThảoDươngTV","TàiChínhPhậtDạy","KinhDighajanu","Shorts"]
  },
  {
    "index": 37,
    "source_title": "Chánh Mạng - Kiếm Tiền Đúng Đạo Đức",
    "title": "5 Nghề Phật Dạy Không Nên Làm - Và Cách Kiếm Tiền Có Đạo Đức Thật Sự #Shorts",
    "hook": "Không phải tất cả cách kiếm tiền đều bình đẳng về mặt đạo đức. Phật phân biệt rõ ràng...",
    "script": "Chào bạn nhen! Chánh Mạng (Samma Ajiva) trong Bát Chánh Đạo: Tránh 5 nghề gây hại: buôn bán vũ khí, buôn người, buôn thịt động vật sống, buôn rượu bia, buôn thuốc độc. Không phải vì nghèo là tốt, mà vì cách kiếm tiền gây khổ đau cho người khác sẽ nuôi dưỡng tâm bất an. Kiếm tiền từ việc tạo ra giá trị thật sự cho người khác mới bền vững và an lạc nhen! Đăng Ký nhen!",
    "category": "Triết Lý Nikaya - Chánh Mạng",
    "tags": ["NikayaKinh","ThảoDươngTV","CháinhMạng","ĐạoĐứcNghềNghiệp","Shorts"]
  },
  {
    "index": 38,
    "source_title": "Bốn Cách Sử Dụng Tài Sản Theo Phật Dạy",
    "title": "Phật Dạy Chia Thu Nhập Theo Tỷ Lệ Này: Bạn Đang Sai Ở Bước Nào? #Shorts #NikayaKinh",
    "hook": "Không phải kiếm được nhiều là giàu. Cách tiêu tiền mới quyết định bạn có hạnh phúc không...",
    "script": "Dạ chào bạn nhen! Trong Tăng Chi Bộ, Phật dạy chia thu nhập thành 4 phần: 1 phần cho nhu cầu thiết yếu. 2 phần đầu tư vào công việc. 1 phần tiết kiệm dự phòng. Và đặc biệt - Phật nhấn mạnh việc bố thí, chia sẻ cho người cần không phải là tiêu xài phung phí mà là đầu tư vào nghiệp lành. Người biết chia sẻ có tâm rộng lượng và hạnh phúc hơn người ôm khư khư nhen! Bấm Đăng Ký nhen!",
    "category": "Triết Lý Nikaya - Quản Lý Tài Sản",
    "tags": ["NikayaKinh","ThảoDươngTV","QuảnLýTiền","TàiChính","Shorts"]
  },
  {
    "index": 39,
    "source_title": "Tinh Tấn - Nỗ Lực Đúng Đắn",
    "title": "Chánh Tinh Tấn: Nỗ Lực Thông Minh Theo Phật Dạy Khác Gì Làm Việc Kiệt Sức? #Shorts",
    "hook": "Làm việc 16 tiếng mỗi ngày không phải tinh tấn. Đây là sự khác biệt mà Phật dạy...",
    "script": "Chào bạn nhen! Chánh Tinh Tấn trong Bát Chánh Đạo có 4 loại: Ngăn điều ác chưa sinh, Diệt điều ác đã sinh, Phát triển điều thiện chưa sinh, Duy trì điều thiện đã sinh. Không phải nỗ lực bất kể hậu quả, mà là nỗ lực có định hướng và cân bằng. Như người chèo thuyền - không phải chèo càng mạnh càng tốt mà phải chèo đúng hướng nhen! Đăng Ký Kênh Thảo Dương TV nhen!",
    "category": "Triết Lý Nikaya - Chánh Tinh Tấn",
    "tags": ["NikayaKinh","ThảoDươngTV","CháinhTinhTấn","NỗLựcThôngMinh","Shorts"]
  },
  {
    "index": 40,
    "source_title": "Bố Thí Ba La Mật - Sức Mạnh Của Sự Cho Đi",
    "title": "Khoa Học Chứng Minh Điều Phật Dạy 2600 Năm Trước: Cho Đi Làm Bạn Hạnh Phúc Hơn #Shorts",
    "hook": "Nghiên cứu tâm lý học hiện đại chứng minh chính xác điều Phật dạy về hạnh phúc...",
    "script": "Dạ chào bạn nhen! Bố thí (Dana) là hạnh ba la mật đầu tiên trong Nikaya. Khi cho đi, não tiết ra Oxytocin và Serotonin - hormone hạnh phúc. Harvard nghiên cứu 2008 cho 46 người tiền và bảo chi cho bản thân hoặc cho người khác - nhóm cho người khác hạnh phúc hơn đáng kể. Phật dạy điều này không phải để được phước báu, mà vì bản chất của cho đi tự nhiên tạo ra niềm vui nhen! Bấm Đăng Ký nhen!",
    "category": "Triết Lý Nikaya - Bố Thí",
    "tags": ["NikayaKinh","ThảoDươngTV","ChoDiHạnhPhúc","BốThí","Shorts"]
  },
  # --- NHÓM 5: NHẠC THIỀN VÀ TÂM LINH (index 41-50) ---
  {
    "index": 41,
    "source_title": "Thiền Mettā - Tu Tập Tâm Từ",
    "title": "[Thiền 5 Phút] Tâm Từ Mettā: Gửi Yêu Thương Đến Bản Thân Và Mọi Người #Shorts",
    "hook": "Chỉ 5 phút thực hành này mỗi ngày sẽ thay đổi cách bạn nhìn bản thân và người xung quanh...",
    "script": "Dạ chào bạn nhen! Cùng Thảo Dương thực hành thiền Mettā nhé. Hít thở nhẹ nhàng... Lặp thầm trong tâm: 'Cầu cho tôi được hạnh phúc - Cầu cho tôi được bình an - Cầu cho tôi không khổ đau'. Rồi mở rộng ra: 'Cầu cho tất cả chúng sinh được hạnh phúc - được bình an - không khổ đau'. Chỉ 5 phút mỗi sáng, não bộ và tim bạn sẽ thay đổi dần theo hướng từ bi hơn nhen! Đăng Ký Kênh nhen!",
    "category": "Triết Lý Nikaya - Thiền Mettā",
    "tags": ["NikayaKinh","ThảoDươngTV","ThiềnMettā","TâmTừ","Shorts"]
  },
  {
    "index": 42,
    "source_title": "Thiền Quán Hơi Thở Anapanasati",
    "title": "[Hướng Dẫn] Thiền Hơi Thở Anapanasati 3 Phút Cho Người Mới Bắt Đầu #Shorts #ThiềnĐịnh",
    "hook": "Kỹ thuật thiền này đơn giản đến mức ai cũng làm được - nhưng lại cực kỳ hiệu quả...",
    "script": "Chào bạn nhen! Anapanasati - Thiền Chánh Niệm Hơi Thở. Ngồi thoải mái, lưng thẳng. Nhắm mắt hoặc nhìn xuống mặt đất. Chú ý cảm giác hơi thở vào ra tại lỗ mũi. Không cần điều chỉnh - chỉ quan sát. Khi tâm lang thang, nhẹ nhàng đưa về hơi thở. Làm 3 phút mỗi ngày trong 21 ngày. Não bạn sẽ dần có khả năng tập trung và bình tĩnh hơn rất nhiều nhen! Bấm Đăng Ký nhen!",
    "category": "Triết Lý Nikaya - Thiền Hơi Thở",
    "tags": ["NikayaKinh","ThảoDươngTV","Anapanasati","ThiềnHơiThở","Shorts"]
  },
  {
    "index": 43,
    "source_title": "Sáu Pháp Thiền Trong Kinh Nikaya",
    "title": "[Nhạc Thiền 432Hz] Tần Số Chữa Lành Giúp Não Bộ Nghỉ Ngơi Sau Ngày Dài Mệt Mỏi #Shorts",
    "hook": "Sau 8 tiếng làm việc căng thẳng, não bạn cần được nghỉ ngơi đúng cách như thế này...",
    "script": "Dạ chào bạn buổi tối nhen... Đeo tai nghe vào, thả lỏng vai và cổ, buông bỏ tất cả những lo toan của ngày hôm nay. Âm thanh 432Hz này theo Phật giáo và một số nghiên cứu hiện đại giúp não bộ chuyển sang trạng thái alpha thư giãn. Cứ thả lỏng và để âm thanh dẫn bạn vào giây phút bình yên tuyệt đối. Chúc bạn có giấc ngủ sâu và ngày mai khỏe khoắn nhen! Đăng Ký Kênh nhen!",
    "category": "Triết Lý Nikaya - Nhạc Thiền 432Hz",
    "tags": ["NikayaKinh","ThảoDươngTV","NhạcThiền432Hz","ChữaLành","Shorts"]
  },
  {
    "index": 44,
    "source_title": "Quán Thân Trong Tứ Niệm Xứ",
    "title": "Body Scan Theo Phật Dạy: Kỹ Thuật 5 Phút Giải Phóng Căng Thẳng Trong Cơ Thể #Shorts",
    "hook": "Căng thẳng không chỉ trong đầu - nó đang nằm trong cơ bắp, cổ, lưng, bụng của bạn...",
    "script": "Chào bạn nhen! Kayanupassana trong Tứ Niệm Xứ là thiền quán thân. Thực hành: Từ đỉnh đầu, di chuyển sự chú ý chậm rãi từng phần cơ thể xuống. Đầu - cổ - vai - ngực - tay - bụng - đùi - chân. Ở đâu thấy căng cứng, hít thở và quan sát cảm giác đó. Không cần thay đổi gì, chỉ quan sát. Sau 5-10 phút, cơ thể tự động thả lỏng một cách kỳ diệu nhen! Bấm Đăng Ký nhen!",
    "category": "Triết Lý Nikaya - Thiền Quán Thân",
    "tags": ["NikayaKinh","ThảoDươngTV","BodyScan","ThiềnQuánThân","Shorts"]
  },
  {
    "index": 45,
    "source_title": "Hạnh Phúc Tỉnh Thức Trong Đời Sống Hàng Ngày",
    "title": "7 Thói Quen Buổi Sáng Theo Triết Lý Phật Giáo Để Bắt Đầu Ngày Hoàn Hảo #Shorts",
    "hook": "Buổi sáng là khoảng vàng định hình cả ngày của bạn. Phật giáo có công thức khoa học cho điều này...",
    "script": "Dạ chào bạn nhen! 7 thói quen sáng theo Nikaya: 1-Thức dậy chánh niệm - không xem điện thoại ngay. 2-Uống nước ấm chánh niệm. 3-Thiền 5 phút quan sát hơi thở. 4-Mỉm cười và biết ơn 3 điều. 5-Đặt ý định cho ngày - hôm nay tôi muốn thực hành điều gì tốt đẹp? 6-Ăn sáng chậm rãi và tỉnh thức. 7-Di chuyển cơ thể ít nhất 10 phút. Bắt đầu thử ngay ngày mai nhen! Đăng Ký Kênh nhen!",
    "category": "Triết Lý Nikaya - Thói Quen Buổi Sáng",
    "tags": ["NikayaKinh","ThảoDươngTV","ThóiQuentSáng","MorningRoutine","Shorts"]
  },
  {
    "index": 46,
    "source_title": "Kinh Metta Sutta - Bài Kinh Tâm Từ",
    "title": "Câu Kinh 2600 Năm Này Thay Đổi Não Bộ: Toàn Bộ Bản Dịch Metta Sutta #Shorts #NikayaKinh",
    "hook": "Bài kinh ngắn này được Phật dạy như thuốc chữa sợ hãi và lo âu - khoa học hiện đại đang nghiên cứu...",
    "script": "Chào bạn nhen! Metta Sutta - Bài Kinh Tâm Từ ngắn nhất và mạnh nhất trong Nikaya. Hãy cùng đọc và cảm nhận: 'Cầu tất cả chúng sinh được sống an vui và hạnh phúc. Cầu tất cả chúng sinh không khổ đau, không oán thù. Cầu tất cả chúng sinh dù đang sống hay đã qua đời, đều được an lành'. Tụng bài này 5 phút mỗi ngày sẽ dần thay đổi cảm xúc và cách nhìn về cuộc đời nhen! Bấm Đăng Ký nhen!",
    "category": "Triết Lý Nikaya - Metta Sutta",
    "tags": ["NikayaKinh","ThảoDươngTV","MettaSutta","KinhTâmTừ","Shorts"]
  },
  {
    "index": 47,
    "source_title": "Học Cách Chấp Nhận Sự Mất Mát",
    "title": "Làm Thế Nào Để Không Đau Khi Mất Đi Thứ Quan Trọng? Phật Dạy Điều Này #Shorts",
    "hook": "Mất mát là điều ai cũng trải qua. Nhưng có người vượt qua nhanh hơn. Bí quyết là gì?",
    "script": "Dạ chào bạn nhen! Trong Udana, một bà mẹ ôm xác con khóc lóc đến Phật xin thuốc. Phật bảo hãy đi tìm hạt mù tạt từ ngôi nhà chưa từng có người chết. Bà đi hỏi khắp làng mà không tìm được. Lúc đó bà hiểu: Mọi người đều đã mất mát như mình. Sự chia sẻ cộng đồng về đau khổ chung này giúp người ta vượt qua nhanh hơn rất nhiều nhen! Đăng Ký nhen!",
    "category": "Triết Lý Nikaya - Vượt Qua Mất Mát",
    "tags": ["NikayaKinh","ThảoDươngTV","VượtQuaMấtMát","KisaGotami","Shorts"]
  },
  {
    "index": 48,
    "source_title": "Tâm Hoan Hỷ - Vui Khi Người Khác Vui",
    "title": "Ganh Tỵ Với Thành Công Của Người Khác? Phật Có Bài Thuốc Đặc Trị Cho Bạn #Shorts",
    "hook": "Ganh tỵ là nọc độc tự đầu độc mình trong khi cố hại người khác. Có cách thoát ra...",
    "script": "Chào bạn nhen! Mudita - Tâm Hoan Hỷ trong Tứ Vô Lượng Tâm: Vui khi thấy người khác hạnh phúc và thành công. Điều này nghe khó nhưng thực ra giải phóng ta khỏi chính ganh tỵ. Thực hành: Khi thấy ai thành công, thay vì so sánh hãy nghĩ 'Họ xứng đáng được điều này. Tôi cũng có thể tạo ra hạnh phúc cho chính mình'. Mudita biến kẻ thù thành bạn và biến ghen tỵ thành động lực nhen! Bấm Đăng Ký nhen!",
    "category": "Triết Lý Nikaya - Tâm Hoan Hỷ",
    "tags": ["NikayaKinh","ThảoDươngTV","Mudita","HoanHỷ","Shorts"]
  },
  {
    "index": 49,
    "source_title": "Tứ Niệm Xứ - Bốn Nền Tảng Chánh Niệm",
    "title": "Phật Tự Nói Đây Là Con Đường Duy Nhất - Tứ Niệm Xứ Là Gì? #Shorts #NikayaKinh",
    "hook": "Có một bài kinh Phật tự nói 'đây là con đường duy nhất đến giác ngộ'. Đó là bài kinh nào?",
    "script": "Dạ chào bạn nhen! Trong Đại Niệm Xứ Kinh, Phật nói: Đây là con đường duy nhất (Ekayano Maggo). Tứ Niệm Xứ gồm: Quán Thân (cơ thể), Quán Thọ (cảm giác), Quán Tâm (tâm trạng), Quán Pháp (các hiện tượng). Thực hành quan sát 4 điều này không phán xét, liên tục trong mọi hoạt động. Không cần ngồi thiền riêng - có thể thực hành ngay khi đang làm việc, ăn uống nhen! Đăng Ký nhen!",
    "category": "Triết Lý Nikaya - Tứ Niệm Xứ",
    "tags": ["NikayaKinh","ThảoDươngTV","TứNiệmXứ","CháinhNiệm","Shorts"]
  },
  {
    "index": 50,
    "source_title": "Lời Cuối - Con Đường Phật Pháp Cho Đời Sống Hiện Đại",
    "title": "Bạn Đã Sẵn Sàng Bắt Đầu Hành Trình Khám Phá Triết Lý Nikaya Chưa? #Shorts #NikayaKinh",
    "hook": "Hàng triệu người trên thế giới đang áp dụng triết lý Nikaya vào cuộc sống hiện đại...",
    "script": "Chào bạn nhen! Hành trình khám phá Kinh Nikaya không cần bạn phải xuất gia hay từ bỏ cuộc sống hiện tại. Chỉ cần 5-10 phút mỗi ngày học và thực hành một điều nhỏ. Vô thường, Duyên khởi, Tứ Diệu Đế, Bát Chánh Đạo - đây không phải giáo điều cứng nhắc mà là công cụ thực tế giúp bạn sống bình an hơn, quyết định thông minh hơn. Hãy bấm Đăng Ký Kênh Thảo Dương TV để cùng nhau trên hành trình này nhen!",
    "category": "Triết Lý Nikaya - Tổng Kết",
    "tags": ["NikayaKinh","ThảoDươngTV","TriếtLýNikaya","HànhTrình","Shorts"]
  }
]

# ==========================================
# 200 BÀI VIDEO DÀI - KỊCH BẢN ĐẦY ĐỦ
# ==========================================
# Đọc 30 bài cũ để tiếp tục đánh số từ 31
existing = []
existing_file = os.path.join(SCRATCH_DIR, "nikaya_30_authentic_posts.json")
if os.path.exists(existing_file):
    with open(existing_file, "r", encoding="utf-8") as f:
        existing = json.load(f)

posts_200 = []
templates_200 = [
  # NHÓM A: TỨ DIỆU ĐẾ & BÁT CHÁNH ĐẠO (31-50)
  ("Khổ Đế - Chân Lý Về Khổ Đau", "Tứ Diệu Đế #1 - Khổ Đế: Tại Sao Phật Dạy Đời Là Khổ Và Đây Không Phải Bi Quan", "Bạn có bao giờ thắc mắc tại sao dù có tất cả vẫn cảm thấy thiếu? Đây là câu trả lời từ Phật giáo."),
  ("Tập Đế - Nguyên Nhân Mọi Khổ Đau", "Tứ Diệu Đế #2 - Tập Đế: Khám Phá Nguồn Gốc Tham Sân Si Làm Khổ Cuộc Đời Bạn", "Ba độc Tham Sân Si đang âm thầm phá hoại hạnh phúc của bạn mỗi ngày. Hãy nhìn thẳng vào chúng."),
  ("Diệt Đế - Niết Bàn Không Phải Cái Chết", "Tứ Diệu Đế #3 - Diệt Đế: Niết Bàn Là Trạng Thái Hạnh Phúc Cao Nhất Không Phải Sự Chết", "Hầu hết mọi người hiểu sai hoàn toàn về Niết Bàn. Sự thật kỳ diệu hơn bạn nghĩ rất nhiều."),
  ("Đạo Đế - Bát Chánh Đạo Thực Hành", "Tứ Diệu Đế #4 - Đạo Đế: Bát Chánh Đạo 8 Bước Thực Hành Thoát Khổ Trong Đời Sống Hiện Đại", "8 bước cụ thể mà Phật dạy. Không cần xuất gia, không cần từ bỏ cuộc sống. Bắt đầu ngay hôm nay."),
  ("Chánh Kiến - Nhìn Đúng Bản Chất Thực Tại", "Chánh Kiến (Samma Ditthi): Cách Nhìn Đời Không Méo Mó - Nền Tảng Của Mọi Tu Tập", "Nếu kính có vết nứt, mọi thứ nhìn qua đó đều bị biến dạng. Chánh Kiến là cách làm sạch kính tâm."),
  ("Chánh Tư Duy - Suy Nghĩ Không Ô Nhiễm", "Chánh Tư Duy (Samma Sankappa): Dọn Sạch Rác Trong Đầu - Tư Duy Đúng Đắn Của Người Trí Tuệ", "Mỗi ngày có hàng ngàn suy nghĩ lướt qua đầu. Chánh Tư Duy là chọn lọc đúng cái nào cần nuôi dưỡng."),
  ("Chánh Ngữ - Nghệ Thuật Ngôn Từ Phật Dạy", "Chánh Ngữ (Samma Vaca): 5 Tiêu Chí Lời Nói Chữa Lành Theo Phật Dạy Cho Người Hiện Đại", "Lời nói có thể xây dựng hoặc phá hủy mối quan hệ chỉ trong vài giây. Phật dạy cách kiểm soát điều này."),
  ("Chánh Nghiệp - Hành Động Đúng Đắn", "Chánh Nghiệp (Samma Kammanta): Hành Động Tạo Nghiệp Lành - Ứng Dụng Thực Tế Trong Công Việc", "Mỗi hành động của bạn đang tạo ra nghiệp - tốt hoặc xấu. Chánh Nghiệp là cách kiểm soát vận mệnh bản thân."),
  ("Chánh Mạng - Kiếm Tiền Có Đạo Đức", "Chánh Mạng (Samma Ajiva): Hướng Dẫn Kiếm Tiền Có Đạo Đức Và Thịnh Vượng Bền Vững Từ Nikaya", "Không phải tất cả cách kiếm tiền đều như nhau về đạo đức. Chánh Mạng giúp bạn thịnh vượng và bình an."),
  ("Chánh Tinh Tấn - Nỗ Lực Đúng Đắn", "Chánh Tinh Tấn (Samma Vayama): Khác Biệt Giữa Nỗ Lực Thông Minh Và Làm Việc Kiệt Sức", "Làm việc 16 tiếng không phải tinh tấn. Đây là sự khác biệt quan trọng mà Phật dạy trong Bát Chánh Đạo."),
  ("Chánh Niệm - Tỉnh Thức Toàn Diện", "Chánh Niệm (Samma Sati): Hướng Dẫn Sống Tỉnh Thức 24/7 Không Cần Ngồi Thiền Riêng Biệt", "Chánh Niệm không phải chỉ ngồi thiền. Đó là trạng thái tỉnh giác trong mọi hoạt động của cuộc sống."),
  ("Chánh Định - Tầng Thiền Định Sâu", "Chánh Định (Samma Samadhi): 4 Tầng Jhana Thiền Định Và Cách Phát Triển Nội Lực Từ Bên Trong", "Thiền định không phải ngồi bất động. Đây là hành trình khám phá 4 tầng tâm thức theo Phật dạy."),
  # NHÓM B: TÂM LÝ & ĐỜI SỐNG HIỆN ĐẠI (51-70)
  ("Đối Phó Với Lo Âu Theo Nikaya", "Phật Dạy Cách Trị Lo Âu: 5 Kỹ Thuật Tâm Lý Từ Kinh Nikaya Cho Người Hiện Đại Bận Rộn", "Lo âu đang ảnh hưởng 1/3 dân số thế giới. Phật giáo có phương pháp điều trị 2600 năm đã được kiểm chứng."),
  ("Trầm Cảm Và Phật Pháp", "Vượt Qua Trầm Cảm Với Trí Tuệ Nikaya: Khi Khoa Học Tâm Lý Hiện Đại Xác Nhận Lời Phật Dạy", "Nhiều liệu pháp tâm lý hiện đại được xây dựng trên nền tảng triết học Phật giáo. Đây là sự kết nối kỳ diệu."),
  ("Mất Ngủ Và Tâm Bình An", "Mất Ngủ Theo Phật Dạy: Thiền Định Và 5 Thực Hành Tối Giúp Ru Ngủ Sâu Từ Kinh Nikaya", "Hàng triệu người mất ngủ mỗi đêm. Nikaya có những hướng dẫn cụ thể giúp tâm an và ngủ ngon."),
  ("Quan Hệ Gia Đình Theo Phật Dạy", "Xây Dựng Gia Đình Hạnh Phúc Theo Kinh Sigalovada: Phật Dạy Các Mối Quan Hệ Thế Tục Như Thế Nào", "Kinh Sigalovada là bản hướng dẫn đầy đủ nhất về các mối quan hệ gia đình và xã hội từ Phật giáo."),
  ("Tình Bạn Chân Thật Theo Nikaya", "Thiện Tri Thức: Tiêu Chí Chọn Bạn Đúng Đắn Và Xây Dựng Tình Bạn Lành Mạnh Từ Nikaya", "Phật nói thiện tri thức là toàn bộ con đường tu tập. Hãy hiểu đúng tiêu chí của người bạn đáng tin cậy."),
  ("Hôn Nhân Theo Phật Dạy", "Phật Dạy Về Tình Yêu Và Hôn Nhân: Kinh Pháp Cú Và Những Nguyên Tắc Vàng Cho Đời Sống Vợ Chồng", "Phật giáo không né tránh chủ đề tình yêu. Đây là những nguyên tắc vàng cho cuộc sống đôi lứa."),
  ("Nuôi Dạy Con Theo Phật Giáo", "Nghệ Thuật Nuôi Dạy Con Theo Triết Lý Phật Giáo: Trồng Cây Đức Hạnh Từ Những Ngày Đầu", "Cha mẹ có thể cho con tất cả vật chất nhưng quên tặng con điều quý giá nhất - nền tảng đạo đức."),
  ("Đối Phó Với Người Khó Chịu", "Làm Thế Nào Khi Làm Việc Với Người Khó Chịu? Nikaya Có 5 Cách Xử Lý Thông Minh", "Ai cũng có người khó tính trong cuộc sống. Nikaya dạy cách duy trì bình an mà không phải né tránh hay đối đầu."),
  ("Tha Thứ Và Buông Bỏ Oán Thù", "Khoa Học Của Sự Tha Thứ: Tại Sao Phật Dạy Tha Thứ Là Quà Tặng Cho Bản Thân, Không Phải Cho Người Kia", "Tha thứ không phải yếu đuối hay cổ súy cho điều sai. Đây là khoa học về sức khỏe tâm lý và thể chất."),
  # NHÓM C: TRIẾT LÝ SÂU VÀ THỰC HÀNH (71-100)
  ("Tam Bảo Phật Pháp Tăng", "Quy Y Tam Bảo Trong Thế Giới Hiện Đại: Phật Pháp Tăng Là Gì Và Tại Sao Quan Trọng Với Bạn", "Quy y không phải lễ nghi hình thức. Đó là sự lựa chọn nhận thức và định hướng sâu sắc trong cuộc sống."),
  ("Nghiệp Và Quả Báo Nhân Quả", "Luật Nhân Quả Trong Phật Giáo: Không Phải Mê Tín Mà Là Khoa Học Về Hành Động Và Hệ Quả", "Luật Nhân Quả không phải lời đe dọa hay phần thưởng. Đó là luật vũ trụ khách quan bạn cần hiểu đúng."),
  ("Tái Sinh Và Luân Hồi Theo Nikaya", "Tái Sinh Trong Phật Giáo Nikaya: Chứng Cứ, Ý Nghĩa Và Cách Sống Có Trách Nhiệm Với Điều Này", "Phật giáo Nguyên Thủy nhìn về tái sinh như thế nào? Và điều này ảnh hưởng cách bạn sống hôm nay ra sao?"),
  ("Ngũ Giới Trong Thế Giới Hiện Đại", "5 Giới Phật Dạy Áp Dụng Thế Nào Trong Thế Giới Hiện Đại? Hướng Dẫn Thực Tế Từng Giới", "Ngũ Giới 2600 năm tuổi vẫn cực kỳ phù hợp với cuộc sống hiện đại. Đây là cách áp dụng thực tế nhất."),
  ("Pháp Cú - Tinh Hoa Triết Lý Phật", "Kinh Pháp Cú (Dhammapada): 50 Câu Kệ Tinh Hoa Nhất Và Ý Nghĩa Sâu Xa Cho Cuộc Sống Hôm Nay", "423 câu kệ trong Pháp Cú là kho tàng trí tuệ dày đặc nhất của Phật giáo. Hãy khám phá 50 câu nổi tiếng nhất."),
  ("Trung Bộ Kinh - Những Bài Giảng Nổi Tiếng", "Những Bài Giảng Nổi Tiếng Nhất Trong Trung Bộ Kinh: Từ Kinh Tổng Quan Đến Kinh Phân Biệt", "Trung Bộ Kinh gồm 152 bài kinh. Đây là 10 bài kinh quan trọng nhất bạn nên đọc và hiểu đúng."),
  ("Tương Ưng Bộ Kinh - Bộ Kinh Chủ Đề", "Tương Ưng Bộ Kinh: Giải Mã Bộ Kinh Có Hệ Thống Chủ Đề Hoàn Chỉnh Nhất Của Phật Giáo Nguyên Thủy", "Tương Ưng Bộ được tổ chức theo chủ đề - từ vô thường đến duyên khởi. Đây là hướng dẫn đọc thông minh."),
  ("Tăng Chi Bộ Kinh - Giáo Pháp Theo Số", "Tăng Chi Bộ Kinh: Tại Sao Phật Dạy Theo Con Số 1, 2, 3... Và Ý Nghĩa Của Cấu Trúc Đặc Biệt Này", "Tăng Chi Bộ tổ chức giáo pháp theo số lượng - từ 1 pháp đến 11 pháp. Đây là trí tuệ sư phạm xuất chúng."),
  ("Trường Bộ Kinh - Các Bài Kinh Dài", "Trường Bộ Kinh: Khám Phá 34 Bài Kinh Dài Và Sâu Sắc Nhất Trong Kho Tàng Phật Giáo Nguyên Thủy", "Trường Bộ Kinh chứa những bài giảng toàn vẹn nhất của Phật. Đây là cách tiếp cận để không bị lạc trong kho tàng đồ sộ này."),
  ("Tiểu Bộ Kinh - Kho Tàng Đa Dạng", "Tiểu Bộ Kinh: Từ Pháp Cú Đến Trưởng Lão Tăng Kệ - Bản Đồ Kho Tàng Văn Học Phật Giáo", "Tiểu Bộ Kinh có 15 tập với các thể loại văn học phong phú. Đây là hành trình khám phá vẻ đẹp văn học Phật giáo."),
  # NHÓM D: ỨNG DỤNG THỰC TIỄN (101-130)
  ("Thiền Định Cho Người Bận Rộn", "Thiền Định 10 Phút Cho Người Không Có Thời Gian: Phương Pháp Thực Hành Từ Nikaya Phù Hợp Với Hiện Đại", "Bạn không cần ngồi thiền 1 tiếng. Chỉ cần 10 phút đúng cách cũng đủ để thay đổi não bộ."),
  ("Chánh Niệm Khi Làm Việc", "Mindfulness Trong Công Việc: 7 Kỹ Thuật Từ Nikaya Giúp Làm Việc Hiệu Quả Hơn Và Ít Căng Thẳng Hơn", "Làm việc chánh niệm không phải làm chậm hơn. Đó là cách tập trung sâu hơn và ít lãng phí năng lượng hơn."),
  ("Quản Lý Thời Gian Theo Phật", "Phật Dạy Gì Về Quản Lý Thời Gian? Bài Học Từ Vô Thường Giúp Bạn Sử Dụng Thời Gian Khôn Ngoan", "Vô thường dạy ta rằng thời gian không chờ ai. Đây là cách quản lý thời gian từ triết học Phật giáo."),
  ("Giảm Stress Bằng Chánh Niệm", "8 Bước Giảm Stress Theo Chương Trình MBSR: Khi Y Học Hiện Đại Ứng Dụng Thiền Phật Giáo", "MBSR - chương trình giảm stress bằng chánh niệm đang được dạy tại 750+ bệnh viện thế giới. Nguồn gốc từ Phật giáo."),
  ("Tập Thể Dục Chánh Niệm", "Yoga Phật Giáo Và Thiền Đi Kinh Hành: Khi Cơ Thể Và Tâm Trí Vận Động Cùng Nhau", "Thiền không chỉ ngồi bất động. Kinh hành - thiền đi bộ - là thực hành chánh niệm trong chuyển động."),
  ("Ăn Uống Chánh Niệm Theo Phật", "Ăn Uống Như Người Tu Tập: Phương Pháp Chánh Niệm Khi Ăn Từ Nikaya Và Lợi Ích Khoa Học", "Cách bạn ăn uống phản ánh trạng thái tâm lý. Ăn chánh niệm không chỉ tốt cho tiêu hóa mà còn cho tâm trí."),
  ("Giao Tiếp Theo Phật Dạy", "4 Nguyên Tắc Giao Tiếp Phi Bạo Lực Theo Nikaya: Khi Nói Chuyện Là Hành Thiền", "Mỗi cuộc trò chuyện là cơ hội thực hành Chánh Ngữ. Đây là 4 nguyên tắc biến giao tiếp thành thiền định."),
  ("Lãnh Đạo Theo Phật Giáo", "Lãnh Đạo Với Trái Tim Rộng Lượng: 7 Phẩm Chất Lãnh Đạo Theo Kinh Nikaya Cho Thế Giới Hiện Đại", "Lãnh đạo tốt không phải kẻ mạnh nhất mà là người có trí tuệ và từ bi nhất. Nikaya dạy điều này từ ngàn năm."),
  ("Sáng Tạo Và Thiền Định", "Mối Liên Hệ Giữa Thiền Định Và Sáng Tạo: Tại Sao Nhiều Nhà Sáng Tạo Lớn Thực Hành Thiền Phật Giáo", "Einstein, Steve Jobs, Arianna Huffington... đều thiền. Khoa học thần kinh học giải thích tại sao thiền kích thích sáng tạo."),
  ("Học Tập Hiệu Quả Theo Phật", "Học Như Người Tu Tập: Chánh Tinh Tấn Và 5 Nguyên Tắc Học Tập Hiệu Quả Từ Triết Lý Nikaya", "Sinh viên ở những quốc gia Phật giáo có điểm học tập cao hơn trung bình. Phương pháp học theo Nikaya là gì?"),
  # NHÓM E: TRIẾT LÝ NÂNG CAO (131-160)
  ("Phân Tích Ngũ Uẩn", "Ngũ Uẩn (Pañcakkhandha): Phật Phân Tích Con Người Thành 5 Thành Phần Ra Sao Và Ý Nghĩa Của Điều Này", "Bạn không phải là cái bạn nghĩ bạn là. Phật phân tích con người thành 5 uẩn - đây là khám phá tâm lý học sâu sắc."),
  ("Lý Duyên Khởi 12 Nhân Duyên", "12 Nhân Duyên (Paticca-samuppada): Vòng Tròn Sinh Tử Và Cách Thoát Ra Từ Kinh Nikaya", "12 nhân duyên giải thích toàn bộ vòng tròn sinh tử luân hồi. Đây là kiến trúc phức tạp nhất của triết học Phật giáo."),
  ("Thất Giác Chi - 7 Yếu Tố Giác Ngộ", "7 Yếu Tố Giác Ngộ (Bojjhanga): Con Đường Phát Triển Tâm Linh Theo Từng Bước Rõ Ràng Từ Nikaya", "7 giác chi là lộ trình rõ ràng từ người bình thường đến giác ngộ. Đây là bản đồ tu tập chi tiết nhất."),
  ("Tứ Niệm Xứ Toàn Diện", "Tứ Niệm Xứ: Hướng Dẫn Thực Hành Đầy Đủ 4 Nền Tảng Chánh Niệm Từ Kinh Mahasatipatthana", "Kinh Mahasatipatthana được Phật nói là con đường duy nhất. Đây là hướng dẫn thực hành đầy đủ nhất."),
  ("Tứ Như Ý Túc - 4 Nền Tảng Thành Công", "4 Nền Tảng Thành Công Theo Nikaya: Tứ Như Ý Túc Giúp Bạn Đạt Được Mọi Mục Tiêu Bền Vững", "Muốn (Chanda), Tinh tấn (Viriya), Tâm (Citta), Quán sát (Vimansa) - 4 nền tảng này đảm bảo thành công bền vững."),
  ("Ngũ Căn - 5 Năng Lực Tâm Linh", "5 Năng Lực Tâm Linh (Pañcindriya): Cách Phát Triển Tín Tấn Niệm Định Tuệ Theo Thứ Tự Đúng Đắn", "Tín, Tấn, Niệm, Định, Tuệ - 5 năng lực này cần được phát triển cân bằng. Mất cân bằng sẽ gây ra những vấn đề cụ thể."),
  ("Ngũ Lực - Sức Mạnh Tâm Linh", "5 Sức Mạnh Tâm Linh (Pañcabala): Khi Năng Lực Tu Tập Trở Thành Sức Mạnh Không Thể Đảo Ngược", "Ngũ Căn khi được tu tập đủ mạnh sẽ trở thành Ngũ Lực - sức mạnh không thể bị lung lay bởi ngoại cảnh."),
  ("Thất Thánh Tài - 7 Của Cải Thánh", "7 Loại Của Cải Thật Sự Theo Phật Dạy: Những Gì Không Ai Có Thể Cướp Đi Từ Bạn", "Tiền bạc có thể mất. Nhưng 7 loại của cải thánh - tín, giới, tàm quý, thính học, bố thí, tuệ - không ai lấy được."),
  ("Tứ Vô Lượng Tâm Thực Hành", "Thiền Tứ Vô Lượng Tâm: Hướng Dẫn Thực Hành Từ Bi Hỷ Xả 4 Tuần Thay Đổi Cuộc Đời", "4 tuần thực hành có hệ thống Từ Bi Hỷ Xả. Các nghiên cứu khoa học cho thấy điều gì xảy ra với não bộ."),
  ("Thiền Từ Bi - Loving Kindness", "Thiền Mettā Bhāvanā: Khoa Học Đằng Sau Thực Hành Tâm Từ Và Cách Thay Đổi Não Bộ Theo Hướng Tích Cực", "Richard Davidson tại Harvard chứng minh thiền Mettā thay đổi cấu trúc não. Đây là nghiên cứu và cách thực hành."),
  # NHÓM F: CÂU CHUYỆN & BÀI HỌC SỐNG (161-200)
  ("Chuyện Kisagotami - Vượt Qua Mất Mát", "Câu Chuyện Kisagotami: Bài Học Về Vô Thường Và Cách Vượt Qua Mất Mát Người Thân Yêu", "Câu chuyện xúc động nhất trong Nikaya về một người mẹ mất con và hành trình tìm đến giác ngộ."),
  ("Chuyện Angulimala - Sức Mạnh Chuyển Hóa", "Angulimala - Kẻ Sát Nhân Trở Thành Thánh Nhân: Bài Học Về Sức Mạnh Chuyển Hóa Không Giới Hạn", "Angulimala từng giết 999 người. Rồi gặp Phật và thay đổi hoàn toàn. Bài học về khả năng chuyển hóa con người."),
  ("Chuyện Ambapali - Vô Thường Và Sắc Đẹp", "Ambapali - Kỹ Nữ Trở Thành A La Hán: Bài Học Vô Thường Từ Người Đẹp Nhất Thành Phố Vesali", "Ambapali đổi rừng xoài lấy một bữa cơm với Phật. Câu chuyện về ưu tiên trong cuộc sống."),
  ("Chuyện Nandaka - Dạy Học Trò Đúng Cách", "Trưởng Lão Nandaka Dạy Nữ Tu: Bài Học Về Sư Phạm Tâm Linh Và Cách Truyền Đạt Trí Tuệ", "Phật yêu cầu Nandaka dạy cho 500 nữ tu. Cách ông dạy và kết quả là bài học tuyệt vời về sư phạm."),
  ("Chuyện Bahiya - Giác Ngộ Trong Khoảnh Khắc", "Bahiya - Người Giác Ngộ Nhanh Nhất Trong Lịch Sử Phật Giáo: Bài Kinh Ngắn Nhất Thay Đổi Mọi Thứ", "Bahiya đi hàng ngàn km để gặp Phật. Và giác ngộ chỉ sau vài câu ngắn. Đây là bài kinh kỳ diệu nhất."),
  ("Chuyện Ratthapala - Từ Bỏ Hoàng Cung", "Ratthapala - Chàng Trai Giàu Từ Bỏ Tất Cả: Đối Thoại Sâu Sắc Về Bản Chất Của Hạnh Phúc", "Ratthapala từ bỏ gia đình giàu có để xuất gia. Cuộc đối thoại với vua sau đó là triết học sâu sắc nhất."),
  ("Chuyện Dhaniya - Người Chăn Bò Và Phật", "Dhaniya Và Phật - Đối Thoại Giữa Hai Lối Sống: Bài Học Về Tự Do Và Trách Nhiệm", "Người chăn bò Dhaniya tự mãn với cuộc sống an toàn. Phật đặt câu hỏi thách thức sâu sắc về ý nghĩa tự do."),
  ("Chuyện Malunkyaputta - Câu Hỏi Vô Ích", "Malunkyaputta Và Những Câu Hỏi Siêu Hình: Tại Sao Phật Từ Chối Trả Lời Một Số Câu Hỏi", "Phật từ chối trả lời 14 câu hỏi siêu hình. Không phải vì không biết, mà vì câu trả lời không có ích cho giải thoát."),
  ("Chuyện Sona - Dây Đàn Vừa Đủ", "Sona Và Bài Học Dây Đàn: Triết Lý Trung Đạo Qua Câu Chuyện Người Chơi Đàn Xuất Gia", "Sona tinh tấn đến mức bàn chân chảy máu. Phật dạy bài học về dây đàn - nền tảng của Trung Đạo."),
  ("Chuyện Kệ Già - Thân Này Vô Thường", "80 Tuổi Phật Tổng Kết Cuộc Đời: Bài Kệ Về Thân Già Và Trí Tuệ Bất Diệt Từ Kinh Trường Bộ", "Trước khi nhập Niết Bàn, Phật đọc bài kệ về thân già. Lời cuối của bậc đại trí là trí tuệ không thể thay thế."),
  ("Phật Nhập Niết Bàn - Những Giờ Cuối", "Những Giờ Cuối Cùng Của Đức Phật: Kinh Mahaparinibbana Và Những Lời Dạy Trước Khi Ra Đi", "Kinh Mahaparinibbana ghi lại chi tiết những ngày và giờ cuối của Đức Phật. Đây là văn học và triết học đỉnh cao."),
  ("Phật Và Khoa Học Hiện Đại", "Khi Khoa Học Gặp Phật Pháp: 10 Điều Phật Dạy 2600 Năm Trước Mà Khoa Học Mới Chứng Minh Được", "Neuroscience, tâm lý học, vật lý lượng tử... đang dần xác nhận những gì Phật dạy. Đây là cuộc gặp gỡ kỳ diệu."),
  ("Phật Giáo Nguyên Thủy Và Phát Triển", "Theravada vs Mahayana: Sự Khác Biệt Và Điểm Chung Của Hai Truyền Thống Phật Giáo Lớn", "Hai nhánh Phật giáo lớn không phải đối nghịch. Đây là cái nhìn khách quan và tôn trọng về sự phong phú Phật pháp."),
  ("Thiền Định Trong Lịch Sử", "Lịch Sử 2600 Năm Thiền Định: Từ Bodh Gaya Đến Phong Trào Mindfulness Toàn Cầu Hiện Đại", "Thiền đi từ Ấn Độ đến Tây Tạng, Trung Quốc, Nhật Bản, rồi đến Mỹ và toàn thế giới. Hành trình kỳ diệu này."),
  ("Phật Giáo Và Môi Trường", "Phật Giáo Và Biến Đổi Khí Hậu: Triết Lý Tôn Trọng Thiên Nhiên Từ Nikaya Và Trách Nhiệm Hôm Nay", "Phật giáo có quan điểm độc đáo về mối quan hệ con người và thiên nhiên. Điều này cực kỳ cần thiết hiện nay."),
  ("Phật Giáo Và Bình Đẳng Giới", "Tỳ Khưu Ni Và Bình Đẳng Giới Trong Phật Giáo Nguyên Thủy: Sự Thật Lịch Sử Ít Người Biết", "Phật thành lập Tăng đoàn nữ - điều cách mạng nhất thế giới thời đó. Lịch sử và ý nghĩa hiện đại của điều này."),
  ("Tổng Kết Hành Trình Nikaya", "Từ Nikaya Đến Cuộc Sống Hiện Đại: Tổng Kết Hành Trình Khám Phá Triết Lý Phật Giáo Nguyên Thủy", "Sau hành trình dài khám phá Nikaya, đây là những bài học cốt lõi nhất để áp dụng ngay vào cuộc sống thực tế."),
  ("Bắt Đầu Tu Tập Như Thế Nào", "Hướng Dẫn Toàn Diện Cho Người Mới: Bắt Đầu Tu Tập Phật Pháp Từ Zero Đến Hero Trong 90 Ngày", "Lộ trình 90 ngày bắt đầu tu tập: từ hiểu lý thuyết cơ bản đến xây dựng thói quen thực hành hàng ngày."),
  ("Tài Nguyên Học Phật Pháp", "Kho Tài Nguyên Học Phật Pháp: Sách, App, Podcast, Website Uy Tín Nhất Cho Người Học Nikaya", "Từ app thiền Insight Timer đến sách Bhikkhu Bodhi - danh sách curated tốt nhất để học Phật pháp hiệu quả."),
]

categories = [
  "Triết Lý Nikaya - Tứ Diệu Đế", "Triết Lý Nikaya - Bát Chánh Đạo",
  "Triết Lý Nikaya - Tâm Lý Ứng Dụng", "Triết Lý Nikaya - Đời Sống Thực Tiễn",
  "Triết Lý Nikaya - Triết Lý Sâu", "Triết Lý Nikaya - Câu Chuyện Phật Giáo",
]

for i, (source, title, hook) in enumerate(templates_200):
    idx = 31 + i
    cat_idx = i % len(categories)
    script_base = f"Kính chào bạn nhen! Hôm nay Thảo Dương chia sẻ về chủ đề: {source}. " \
                  f"{hook} " \
                  f"Theo Kinh Nikaya, đây là một trong những bài học quan trọng nhất cho cuộc sống hiện đại. " \
                  f"Hãy cùng khám phá và áp dụng những tri thức này vào thực tế cuộc sống của bạn. " \
                  f"Nhớ Đăng Ký Kênh Thảo Dương TV để nhận video mới mỗi ngày nhen!"
    
    posts_200.append({
        "post_index": idx,
        "source_title": source,
        "title": title,
        "hook": hook,
        "script": script_base,
        "category": categories[cat_idx],
        "slot": ["slot_18pm", "slot_20pm", "slot_2130pm"][i % 3],
        "tags": ["NikayaKinh", "ThảoDươngTV", "TriếtLýNikaya", "Phật Dạy", "1995lido"]
    })

# Gộp với 30 bài cũ
all_posts = existing + posts_200

# Lưu file 200+ bài
output_posts_file = os.path.join(SCRATCH_DIR, "nikaya_230_authentic_posts.json")
with open(output_posts_file, "w", encoding="utf-8") as f:
    json.dump(all_posts, f, ensure_ascii=False, indent=2)
print(f"✅ Đã lưu {len(all_posts)} bài video dài vào: nikaya_230_authentic_posts.json")

# Lưu 50 shorts
existing_shorts = []
existing_shorts_file = os.path.join(SCRATCH_DIR, "nikaya_10_shorts.json")
if os.path.exists(existing_shorts_file):
    with open(existing_shorts_file, "r", encoding="utf-8") as f:
        existing_shorts = json.load(f)

all_shorts = existing_shorts + shorts_60
output_shorts_file = os.path.join(SCRATCH_DIR, "nikaya_60_shorts.json")
with open(output_shorts_file, "w", encoding="utf-8") as f:
    json.dump(all_shorts, f, ensure_ascii=False, indent=2)
print(f"✅ Đã lưu {len(all_shorts)} kịch bản Short vào: nikaya_60_shorts.json")

# Thống kê
print("\n" + "="*60)
print("📊 THỐNG KÊ KHO NỘI DUNG")
print("="*60)
print(f"📱 Shorts Video (60s): {len(all_shorts)} kịch bản")
print(f"🎬 Video Dài:          {len(all_posts)} kịch bản")
print(f"📅 Đủ phát 5 video/ngày trong: {len(all_posts)//5} ngày ({len(all_posts)//5//30} tháng)")
print(f"⏰ Upload Short 1h/lần trong:  {len(all_shorts)} giờ ({len(all_shorts)//24} ngày)")
print("="*60)
