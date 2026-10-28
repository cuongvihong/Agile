# Sprint 1 Demo với khách hàng: Transcript

Nguồn: `groundtruth/Sprint 1.m4a`, thời lượng 30 phút 49 giây, metadata ghi lúc 14:36 ngày 2026-10-16 (UTC+7). File là âm thanh m4a, không phải mp4 và không có hình, nên chỉ có lời nói.

Cách tạo: nhận dạng giọng nói tự động bằng Whisper small (chạy qua sherpa-onnx, ép tiếng Anh), cắt đoạn theo khoảng lặng. Đây là bản máy, chưa ai nghe đối chiếu. Mốc thời gian là thời điểm bắt đầu từng đoạn.

## Lưu ý khi đọc

Không có nhãn người nói. Người trình bày là phía team (Dory phần overview, Hayden phần demo, theo cách máy nghe tên), người hỏi và nhận xét được hiểu là khách hàng. Đây là suy luận từ ngữ cảnh: câu cuối của buổi nói "the team can take this back and propose a solution in next week's demo".

Tên người, tên hệ thống và một số thuật ngữ bị nghe sai, xem mục 3. Đoạn 04:06 đến 04:32 là khoảng âm thanh trống nên câu trả lời về việc ghi đè dữ liệu khi sync không có trong bản chữ. Đã bỏ các tiếng đệm và đoạn chỉ có tạp âm. Một đoạn dài hơn 30 giây có thể bị cắt phần cuối (công cụ chỉ đọc 30 giây đầu mỗi đoạn).

## 1. Transcript

**[00:00]** Hi Dory. Yeah, okay. Today our team 5 and 8 will introduce you about the Spring one. I'm Dory, I will in charge of the overview and then after the overview we will run to the demo with Hayden. So first...

**[00:19]** I will introduce you the user type. So here we have divided into two portal which is admin portal as well as eService portal. The admin portal is for MOE HQ.

**[00:33]** as well as the school users.

**[00:36]** the interview is for parents so

**[00:39]** Let's take a look here. The identifications for Amy Poto, they are both in username and password.

**[00:46]** Their primary charge is a little bit different. The MOE hard queue will manage school level class or students, while the school users can configure school offering classes, register students or enrollment.

**[01:04]** So, next is the parent. They can view the student education account details and they can check the fees. They can update profile ads to make the payment.

**[01:16]** So, for the flow, Hayden will give you the demo.

**[01:25]** Hello Yao, I'm Hayden, so now I'm responsible for the team for D-MIL.

**[01:33]** Wait a minute for us to share the demo.

**[01:43]** Do you see the screen now?

**[01:47]** It is this show home page

**[01:51]** We haven't compiled the home page yet, but this is the login page for the MOE and the school user first.

**[02:03]** Here is the login page for the MOE and school user. So here we have the mock data of the MOE first.

**[02:13]** Let me wait to tie.

**[02:19]** So this is the account of the MV headquarters.

**[02:24]** So here as you can see, so this is the

**[02:28]** the homepage of the AMOE account.

**[02:32]** Here we have many functions but we have basically this week we focus on functions 1, 3, 8 and 9.

**[02:42]** Here we have the education account. As mentioned in the function one, the system will automatically send the data of the Singaporean student from 7 to 16. So we do have this function and we add some more features. That is manual things. When we press this button like manual things, it will

**[03:07]** the data from the government.

**[03:11]** right now.

**[03:12]** So here let me take a test.

**[03:21]** Is there any difference between your first manual sync versus all the subsequent sync? So this is maybe the same, but this is manually so when the MWA have to need to get some newest data, so this is for that purpose. But manually every night at 12 p.m. the system will

**[03:46]** updated automatically.

**[03:50]** Do you do a full sync or an incremental sync? It's a full sync.

**[03:57]** So you will override the existing data even if there are no delta changes?

**[04:32]** The next day we will run the job to see the beginning of the day. That's 12 am every day. To see the full data of the citizens who age is 7. That's exactly the way we run the daily job.

**[05:32]** So next up I will present you about the school user function. So here is the function where the MOE headquarters will create the school user. So as I press this button it will create the school user based on three main criteria. First one is EnRid. So it will save it as

**[05:58]** as a single school user here. So when creating school user, we have two functions. First one, we will add a single one or we can have the poll create. So here we can add the CSV file of the list of school user here to add it.

**[06:22]** Frequently yeah for sambo is like this

**[06:30]** So as you can see here, this is a list of school users I have just created right now. So why do you have password? For sign purpose for school users.

**[06:47]** School users, they are supposed to sign in with their SOE account. Is it their AD account? You shouldn't stop password in your system, yeah? You know, that's very sensitive, right? Yeah, I know, because this is from the MOU site, so the MOU will provide it to the school users. No, it's their AD account. It is integrated with their AD account.

**[07:16]** There's no separate username and password. OK. So we will mention it and provide it to you for the next demo. So right now, the spring basically based on the username and password for our skilled user.

**[07:37]** So it can export to the file and send it to the school user based on our current flow.

**[07:46]** So the next step is creating the academic levels.

**[07:56]** So we have this mock data for the name, the education stage, when the MOE creates the education state for configuring the school. So here we're just creating the mock data, so we will describe it to you later. And besides the academic levels, we also provide a function that can create the academic years.

**[08:26]** to identify, to clarify between each class, between years. Like in 2026, there are 10 class is clearly different from 2027 with 10 class. So the main function we build this week is mainly about grade school and the school user I mentioned before.

**[08:53]** So here is also the mock data for MOE for them to create. So as I demonstrate here, when I create a school detail for school user, it has these details like the school code, school name, school type. And you can assign the school user you have created before.

**[09:20]** in the interior school.

**[09:22]** So let me just type this.

**[09:29]** school name

**[09:33]** So the school type here we conflict by five types, the government type, the government aid, the autonomous, the independent and the specialized type.

**[09:48]** So here is a list of users that we have created. Do you have a better way to manage the school users? That's not very effective. There are hundreds of users in a school.

**[10:00]** Right now we just listed like this list. Yeah, I cannot accept this solution. You can go back and think of a new solution for this. Yeah, okay. We'll take it as a note and we'll fix it soon.

**[10:17]** So here you can assign the school user and choose the academic level.

**[10:36]** Actually, what would you display under the school users? Do you display all the users in the system?

**[10:48]** It's based on the which school user we assigned to that school.

**[10:57]** You are assigning the school user to the school on this page, right? Yes. Then how you scope down? My question is actually how you scope down.

**[11:10]** And care while school users belong to multiple schools about.

**[11:20]** Anyways, you can take this back.

**[11:24]** Can one school user belong to multiple schools? For now, we only decide that only one school user is assigned to one school. But one school can have many school users. OK.

**[11:42]** Okay. Okay. Sorry, so let's continue here. So we have, when creating the school, we have a list of school that the MOE will manage.

**[11:57]** Here I just created the UAT1 right here. So it's at zero active class and zero active student. So this is the overview of the M.V. headquarters view. So now I will change to the school user view.

**[12:18]** Let me check a little bit

**[12:31]** Can you wait a minute for me to create a new school for better demo here?

**[12:38]** Okay. Yeah, thank you.

**[12:46]** Next time please create your demo detail in advance, okay? Yeah, okay.

**[13:26]** So this is well well

**[13:45]** Okay, so this is the school user site here. So here the school user have to configure the class and after that they have also, they have the chance to put the student into the class. So their duty right now is to create the class first.

**[14:08]** So the class detail complete the code, the name, and also the school level offering configure before.

**[14:23]** Yes, so right now I just created a class and now I will assign a student to this class.

**[14:33]** So now you have to create a student and then you assign it to the class.

**[14:50]** So we need to set up the day of birth.

**[14:54]** the category of the student.

**[14:59]** So the student category is what we need to add on here to consider the FAS and the field management on the parent site.

**[15:12]** and we have to... Can you call it citizenship instead of student category?

**[15:22]** the field name? Not really because there are some students who are Singaporeans but there are some students who are international students but we don't really find out which country they belong to so I think that using the term citizenship is appropriate here so we just use it.

**[15:48]** That's how we use it. In 6th one we will take note of them and just make it hard.

**[16:06]** So we set up the enrollment start date.

**[16:25]** And then we create a student and...

**[16:31]** Yeah, so here we have the student and we can see it detail here. So I just create the student named Hugh Fang 1. So here the current class is not assigned. And so now we have to assign the class we just created to manage it based on the function tree. So this is a slide I just created before.

**[16:58]** Class 1 and assignments enrollment start.

**[17:06]** tomorrow.

**[17:15]** Yeah, so basically this is a fault that the school user assigned the student into the class and the school user remanded it. Many class and many students. What does the enrollment status mean?

**[17:32]** Enrolled. What does it mean?

**[17:38]** It means they are attending in the school and if there is a case that if the student transfers into another school, the subject will change to transfer to another school and if they graduate, the subject will change to close.

**[18:03]** Okay, do you have a school enrollment that table enrolled from and to where do you get the days from?

**[18:14]** This is based on the student, based on the assumption that the enrolled form is the day that the student start study from the school and the enrolled too is the graduation day.

**[18:32]** How do you know their graduation date is 23 December 2027?

**[18:39]** It's just expected but our system can accept it as a new value and the school user can add it later.

**[18:57]** I think you still need to find a way to indicate an accurate enrollment date. Don't just anyhow put a date there, okay? Okay, yeah. We mentioned that. Thank you. So this is basically the school user view. So now we'll present about the Terran view.

**[19:32]** So this is the...

**[19:35]** The service portal here, so the parent had to sign with the same pass.

**[19:42]** So here we do some mockup data here and just login to it. So when the parent login successfully, the first thing that we will see is their CHI card. So here you can see three cards, which means that this parent managed three children. And the card shows the EA balance. This is the parent view, right? Yep.

**[20:12]** Okay, do you think as a parent they don't know their child's date of birth and citizenship and race and address?

**[20:22]** Our purpose here is to show more than this card like the fee, the outstanding charge, the fee that the parent haven't paid for it. So this is just the...

**[20:39]** Just basic information, we will recover it later.

**[20:44]** So you will still show the basic information? Yes, the field will combine to this card later. Okay, you only have this much of space.

**[20:57]** It's the homepage where parents first log into the system, they will see this homepage. But you are occupying so much space just to display the date of birth, gender, race, citizenship, which the parent already know. No parent would not know their children's basic information. So what I'm saying is you can reserve the space for better usage.

**[21:23]** Okay, if you think that these are not necessary, then we'll try to display another information that is more like necessary so that the parent can view on the whole page.

**[21:38]** and move this information into the student profile section for more details.

**[21:51]** So next up is the Pan-Rofi

**[21:58]** So here's the information of the parent that we integrated from SYNTAS here. The full name, the NRIK, the residential address, the contact information, we get it from the SYNTAS. And here is the mail address that these are basic information that parent can adjust on the system.

**[22:23]** Like here you can change the phone number, email address, the block, the sprit.

**[22:33]** to update to our system.

**[22:42]** So to the transaction

**[22:45]** So here, parents can see the Gai transaction history here, just like this. Go to the fee and payment. So here-- Wait a minute. Can you go back to transaction page? Under what circumstances would the status be not successful?

**[23:12]** Currently we just based on the happy case and about the not success for starters maybe we will revive it for the QA test like the system fail on the network or something and we will revive it to you later.

**[23:29]** Okay, but if it failed, should we still display to parents? Shouldn't we recover those transactions and then display only the successful transactions to parents? Have the team ever think about that? We do discuss about that. Our idea right now is just keep it started.

**[23:56]** and maybe we'll change it, I'll get rid of it for a better parent experience.

**[24:02]** Okay, so let's go to the last part, the fee and payment. So here the parent will have responsibility to see the fee for each of the child, for example here.

**[24:18]** They can see the DARE/JI balance of the EA account. So they also see the outstanding fees. So here is the fee that they asked you to charge. So here, for example, I will pay for it for the standard fee and field trip.

**[24:42]** Here we have two ways for the pay. The first one is using the EAA or we use the online gateway. So here, just use the EAA account, balance, yeah, just auto-run and pay.

**[24:58]** and so it showed the receipt and then we go back here to see and the account has just minus it

**[25:11]** The second method is use the online gateway so here also authorize and pay. Our flow now still not provide the key wall for the parent to pay it so it's just the just simple basic information here will provide it to you next week also.

**[25:33]** Yeah, and then we pay the successful and the system bring out the receipt.

**[25:39]** and then

**[25:40]** It's done up the flow when paying the fee for the check.

**[25:46]** So the flow is you have to choose a child first, is that? Yes.

**[25:51]** And then the outstanding fees and educational balance is for that particular child. Yes.

**[25:58]** All your child is there. Okay. Can display the child's name somewhere else.

**[26:03]** rather than as a card, I thought.

**[26:05]** Right corner. Yeah, we can do that later.

**[26:09]** We mentioned it. Okay. Okay.

**[26:11]** then your outstanding fees is not calculated, it's not updated yet, right?

**[26:18]** After you pay for a fee, your outstanding fees and education account balance should be updated real time. It will be updated real time.

**[26:29]** Oh, okay.

**[26:31]** Maybe I didn't see this.

**[26:34]** So for example, if I select all these fees, the total fee is 840, but we have...

**[26:45]** Oh, that's right.

**[26:49]** Okay, so this basically our...

**[26:54]** And we do provide for you the M.O.E. and school user view before. So that is basically our presentation today for our demo.

**[27:03]** So, um...

**[27:06]** Oh, that's hard. Can you scroll down a bit? I'm sorry, we do have the situation here.

**[27:14]** for assemble

**[27:35]** here so the total fee is like a thousand and a hundred but the EA is just a thousand here so when we go to the payment so we do add on the both payment way so we

**[27:53]** use the bow, ear, cow and also the on-line gateway. So it uses the current.

**[28:00]** education account and add on the online gateway for the parent to finish the total fee here.

**[28:09]** Can you allow me to choose the amount to use for education account? Right now. I may not want to...

**[28:16]** I may not want to use up all the $1,000 oil at once. Okay, so right now we haven't modified it, but if you want we can modify it for you later.

**[28:29]** and then we also write some paint just like the

**[28:33]** Ravus, well

**[28:37]** That's it. So...

**[28:39]** Okay, can you go back to the Outstanding Fee page again? I want the team to look into the UI.

**[28:48]** You see the first column is very narrow. Okay, maybe find another child with data. Okay. Yeah, like this.

**[28:57]** The first column is very narrow, the second column is very wide, but the description of course is not that long. And if you scroll down further...

**[29:11]** The... okay, your educational account balance. Why do you display it here again?

**[29:20]** Yeah, it's... Right? And your date format... Here is year, month, day. I think some of your other pages is a different format.

**[29:32]** So please do date.

**[29:36]** due date format.

**[29:39]** Okay, I'll fix it.

**[29:42]** So this is the overall flow of our system. So do you have any feedback right now?

**[29:53]** I think you may still want to drill down into some of the details. At high level, it may look okay, but there are certain happy scenarios that I think the team haven't really considered yet. And also from user experience perspective, you may also think of what is real, really useful from a parent perspective.

**[30:19]** So the team can take this back and propose a data solution in next week's demo. Yeah, and we'll mention it and enhance it later. Thank you. Okay, so thank you for today, D-Mode. So we'll see you next week. Yeah, thanks team. Bye bye. Bye bye. Thank you, bye bye.

## 2. Phản hồi và câu hỏi của khách trong buổi demo

Đây là phần tôi đọc từ transcript, người nói được gán theo suy luận ở trên. Cột đoạn là mốc thời gian trong mục 1.

| Đoạn | Chủ đề | Nội dung |
|---|---|---|
| 03:21 đến 04:06 | Đồng bộ dữ liệu Education Account | Khách hỏi sync thủ công khác gì sync hằng đêm, full hay incremental, có ghi đè khi không có thay đổi không. Team trả lời là full sync. Câu trả lời về ghi đè rơi vào đoạn âm thanh trống. |
| 06:47 đến 07:36 | Mật khẩu School User | Khách nói School User đăng nhập bằng tài khoản AD của MOE, hệ thống không nên lưu mật khẩu vì rất nhạy cảm. Team nói Sprint này tạm dùng username và password, sẽ cập nhật ở demo sau. |
| 09:48 đến 10:17 | Danh sách School User | Khách hỏi cách quản lý khi một trường có hàng trăm user, nói chưa chấp nhận cách liệt kê hiện tại, yêu cầu nghĩ giải pháp mới. Team ghi nhận. |
| 10:36 đến 11:42 | Phạm vi School User theo trường | Khách hỏi danh sách được giới hạn theo trường như thế nào và một School User có thuộc nhiều trường không. Team: hiện một School User chỉ gán một trường, một trường có nhiều School User. Khách bảo team mang về xem lại. |
| 12:46 | Chuẩn bị demo | Khách nhắc lần sau tạo sẵn dữ liệu demo. |
| 15:12 đến 16:06 | Tên trường Student category | Khách hỏi có thể gọi là citizenship thay cho student category không. Câu trả lời của team bị nghe lẫn, phần cuối nghe như dùng thuật ngữ citizenship. Cần nghe lại. |
| 17:32 đến 18:57 | Enrollment | Khách hỏi ý nghĩa Enrollment status, nguồn của enrolled from và enrolled to, vì sao ngày tốt nghiệp là 23 December 2027. Team nói đó là ngày dự kiến, School User có thể nhập lại. Khách yêu cầu có cách xác định ngày nhập học chính xác, không đặt ngày tùy ý. |
| 20:12 đến 21:48 | Trang chủ phụ huynh | Khách nói thẻ con chiếm nhiều chỗ để hiện ngày sinh, giới tính, chủng tộc, quốc tịch mà phụ huynh đã biết, nên dành chỗ cho thông tin cần hơn như phí còn nợ và chuyển thông tin cơ bản sang trang hồ sơ học sinh. Team đồng ý. |
| 23:08 đến 24:02 | Giao dịch không thành công | Khách hỏi khi nào trạng thái không thành công xuất hiện và có nên hiện giao dịch lỗi cho phụ huynh không. Team: hiện mới làm happy case, sẽ bổ sung kịch bản lỗi mạng cho QA, tạm giữ hiển thị và có thể bỏ sau. |
| 24:42 đến 25:46 | Thanh toán | Team demo trả bằng Education Account và bằng cổng online. Màn của cổng thanh toán chưa làm, hứa tuần sau. |
| 26:03 đến 26:34 | Chọn con và cập nhật số liệu | Khách đề nghị hiện tên con ở nơi khác thay vì chỉ ở thẻ, và hỏi phí còn nợ cùng số dư EA có cập nhật ngay sau khi trả không. Team: có cập nhật theo thời gian thực. |
| 28:09 đến 28:29 | Trả kết hợp EA và online | Khách muốn tự chọn số tiền lấy từ Education Account. Team: chưa làm, sẽ sửa sau. |
| 28:39 đến 29:39 | Trang Outstanding fees | Khách nói cột đầu quá hẹp, cột hai quá rộng, số dư EA bị hiện lại, định dạng ngày năm tháng ngày khác các trang khác. Team sẽ sửa. |
| 29:53 đến 30:19 | Kết luận | Khách nói ở mức tổng quan thì ổn nhưng còn nhiều kịch bản ngoài happy case chưa được xem xét, và cần nghĩ theo góc nhìn phụ huynh. Team mang về và đề xuất giải pháp ở demo tuần sau. |

## 3. Chỗ máy có thể nghe sai

Các mục dưới đây là suy luận, bằng chứng là ngữ cảnh quanh câu và Project Facts trong CLAUDE.md, chưa nghe lại file âm thanh.

| Máy nghe | Có thể là | Bằng chứng |
|---|---|---|
| Spring one | Sprint 1 | Câu mở đầu giới thiệu buổi demo của sprint, timeline dự án ghi Sprint 1 từ 2026-10-11 đến 2026-10-17 |
| MV headquarters, MOE hard queue, MOU, AMOE | MOE HQ | Cùng đoạn nói về admin portal của MOE HQ |
| Terran view | Parent view | Câu ngay trước nói "now we'll present about" phần cho phụ huynh, sau đó chuyển sang eService portal |
| the same pass | SingPass | Project Facts ghi transcript kick-off có lỗi nghe SIMPASS thay cho SingPass, đoạn này nói phụ huynh đăng nhập eService |
| SYNTAS | Chưa rõ | Nói là nơi lấy họ tên, NRIC, địa chỉ của phụ huynh, có thể là dữ liệu mock giả lập SingPass. Cần nghe lại |
| Pan-Rofi, CHI card, EAA, DARE/JI | Profile, child card, EA, số dư EA | Cùng câu nói về trang hồ sơ, thẻ con và Education Account |
| enrolled form, enrolled too | enrolled from, enrolled to | Câu hỏi nói về hai cột ngày của Enrollment |
| Dory, Hayden, Yao, Amy Poto, Hugh Fang 1 | Tên người và tên dữ liệu mẫu | Chỉ là cách máy nghe, chưa xác nhận |
