# Finance System for Ministry of Education (MOE): Agile Project Kick-off

Transcript created on October 09, 2026 at 09:18

## Transcript

**[00:00]** Good afternoon. Hi, well, we're partnered, and now detail: the time frame is limited. Okay, so listen carefully. Okay, yo, please.

**[00:11]** I'm here.

**[00:12]** Hands down.

**[00:12]** I'm not ready yet.

**[00:15]** Okay, let me share my screen.

**[00:20]** Let me know if you're seeing the screen now.

**[00:23]** I don't know.

**[00:25]** Get the word.

**[00:27]** One beat.

**[00:36]** I think Bruce your side need to unmute again, and also share the contact camera because someone just started recording.

**[00:51]** Okay.

**[00:56]** Wait, can you see my screen?

**[00:57]** Yes, I can.

**[01:00]** Okay. Sure. So, um, this will be the agile project that all of you will be working on.

**[01:08]** Yeah, I'm in.

**[01:09]** You all have been assigned different roles. Um, so we are building a finance system for Ministry of Education, MOE. Okay, so, uh, here's the to-do list of requirements that we have. We have 10 items.

**[01:27]** Do we announce them yet?

**[01:29]** First, I'll take you first, okay?

**[01:32]** And we will go one by one. So first of all, uh, we should have the education account module. So the education account is available to Singapore citizens for education-related spending. It should be automatically created and activated when the child turns 7 years old, and automatically close, uh, when the child reaches 16. And then the education account can actually be used for, uh, education-related purposes.

**[02:03]** For example, if the child is studying in, uh, Singapore government schools, then they can use the education account balance to pay for, uh, MOE bill and school bill and so on. Okay? So you may wonder how does the, uh, account, uh, is being managed and how where does the ma-many come from, right? So we actually allow the, uh, headquarter HQ, MOE HQ uses, to perform top-up to the education account. So it can be done in batches or, uh, to specific account holders.

**[02:41]** And, uh, for the batch operation, the HQ, the HQ user should be able to configure rules based on the account holder's age, account balance, uh, schooling status, and the top-up can also be done regularly or on an ad hoc basis. So I can do a yearly top-up, for example. Or if there's, um, special budget approval from the government, then we can also do it on an ad hoc basis.

**[03:12]** Okay? Other than that, the HQ users and school users will also need to maintain the list of schools, the list of government schools, uh, in Singapore, and then the levels of cohorts of each school, uh, the classes of each level, and then the students in each class. And also the type of fees and fee components payable by students. So based on all this different information, we will later we will be able to calculate the, uh, um, bills or the fee payable by each student. Okay? So as I explained earlier, the Singaporean students can actually use the balance in the education account to pay for the school fees.

**[03:58]** Okay? So, uh, the first three user stories actually explain the, uh, the overall picture for the, uh, account hold the education account as well as the usage. Okay? So on top of it, students with financial needs, they can apply for financial assistance scheme, which is short for FAS.

**[04:22]** Um, the system should allow configuration on multiple different schemes. So for example, at MOE level, at the nationwide level, we could have one scheme. And then there could be different eligibility criteria based on student's nationality, household income, per capita income, and also different tiers and the corresponding subsidy amount on different fee components. Um, other than the nationwide, um, FAS, each school is also able to configure their own school-based FAS. Okay? So, uh, you can assume that the income information of each family will come from a third-party system via system interface, via API. Okay?

**[05:08]** So MOE level FAS, it should be automatically granted if the student's family meet the certain predefined, uh, criteria based on, for example, household income as well as per capita income.

**[05:24]** And then if MOE FAS is not granted, then, uh, it goes to each, uh, individual school to decide if they want to, uh, grant school-based FAS to the applicants, to the students. And then the outcome of the FAS application should be reflected in the fee payable.

**[05:47]** So basically, it means that if, let's say, uh, for this month's school bill, I'm supposed to pay $100, but because I'm joining, let's say, school-based FAS, and there's a deduction of $90, so in the end, I should be only paying $10. Okay? So, um, there's, uh, some AI features that we expect out of the system as well. Uh, first of all, there should be rule-based logic to determine the eligibility of the students who are applying for FAS. And then we also expect machine learning to predict the remaining financial difficulty and recommend an appropriate assistance tier. So I think the, uh, model, uh, to classify students, and, uh, it should look into different financial difficulty levels, for example, low, medium, and high. So this part you can read yourself later on. Okay?

**[06:40]** So other than those, um, parents and family who apply for FAS online in the eService portal, um, the system should also support the capturing and processing of hard-copy application forms, which is filled in by students by parents offline.

**[06:58]** And, uh, because some students some parents, they may not have, uh, SIMPASS account to log into the system, therefore they can only fill in on a paper form, and then the school users will actually collect those forms and then, uh, scan and submit into the system.

**[07:16]** Okay? And other than that, we are also expecting some kind of budget tracking and spending statistics on both MOE FAS as well as school-based FAS. Okay? So of course, each school, they are able to determine their budget and, uh, the assignment or allocation or granting of the school-based FAS. And at MOE HQ level, other than the MOE FAS tracking, they should also be able to see how each school is allocating their budget.

**[07:50]** Okay? And in order to assist school users as well as parents better, we are also expecting MOE HQ users to be able to simulate how school users and parents access the system and see the system in order to address their queries.

**[08:06]** Because sometimes they may just, as a parent or even school users, may just come to HQ and say, "I'm encountering certain difficulties," but they can't really see the screen. So that's why we expect HQ users to have this kind of simulation functionality. Okay? So the first seven user stories are, uh, talking about admin portal. Okay? They.

**[08:31]** I mean, the HQ users and school users are expected to log in using their, uh, SSO, uh, single sign-on with the, uh, uh, using their AD account. Okay? So next, we will move on to the eService portal.

**[08:46]** Uh, I think previously we explained that there will be education accounts, and then, um, the parents can actually manage the education accounts on behalf of the child, right, on behalf of their children.

**[08:59]** So, uh, first requirement for the eService portal is that parents should be able to access the eService portal via SIMPASS, log in using SIMPASS, to view the education account details, balance, transactions, and also update some of the basic personal information such as address, residential address, mailing address, contact number, and so on. Okay?

**[09:23]** And they should also be able to view the outstanding charges, and they can choose to pay for the fees using either the balance from education account or via online payment method, for example, credit card, or using a combination of both methods. And of course, they should be able to apply for financial assistance scheme as a family unit. Okay? So they should apply as a family because the essentially, we are assessing the application based on the household income and per capita income. So the application should always come as a family unit. Okay? On top of it, we are also expecting some AI solution to allow users to ask questions related to the functionalities in the eService portal. This is also, again, to assist users better and also dynamically ask follow-up questions in order to better understand the context and provide more relevant answers.

**[10:21]** And other than that, the system should also be able to automatically fill in the FAS application form based on the parent's profile as well as, um, the, uh, answers from previous questions that the system asked and, uh, parents clarified. Okay? So this is the, uh, overall requirements.

**[10:46]** In totality, we are expecting one admin portal and one eService portal, serving different user personas and, uh, some AI, uh, features as well on top of the base functionalities.

**[11:01]** And I think we can open the floor for questions.
