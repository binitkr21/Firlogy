function chatBot() {
	
	// current user input
	this.input;
	
	/**
	 * respondTo
	 * 
	 * return nothing to skip response
	 * return string for one response
	 * return array of strings for multiple responses
	 * 
	 * @param input - input chat string
	 * @return reply of chat-bot
	 */
	this.respondTo = function(input) {
	
		this.input = input.toLowerCase();
		
		if(this.match('(hi|hello|hey|hola|howdy)(\\s|!|\\.|$)'))
			return "um... hi?";
		
		

		if(this.match('can we use this app without having internet?') || this.match('CAN WE USE THIS APP WITHOUT INTERNET?') || this.match('CAN We Use This App Without having Internet?'))
			return "No, One can not use this app without  having Internet Connection.Internet connection is requied to use this app.";

		if(this.match('What does this app do?') || this.match('what does this app do?') || this.match('What does this app do'))
			return "One can register a FIR report  here without going to the Police Station successfully.";
		
		if(this.match('Is smart phone required to use this app?') || this.match('is smart phone required to use this app?') || this.match('Is Smart phone required to use this app?'))
			return "Yes, Smart phone is required to Register a FIR here .";
		
		if(this.match('theft') || this.match('THEIFT') || this.match('THieft'))
			return "What was stolen?";
		
		if(this.match('purse') || this.match('PURSE') || this.match('PURse'))
			return "At what time?";
		
		if(this.match('morning') || this.match('evening') || this.match('afternoon') || this.match('night'))
			return "Ok. Dont worry. Just go to register FIR panel and fill your details there correctly. Your FIR will be registered and you will get all sorts of notifications of how your case has progressed so far.";
		
		if(this.match('kidnapping') || this.match('Kidnapping') || this.match('KiDnapping'))
			return "Who has been kidnapped?";
		
		if(this.match('stranger') || this.match('relative') || this.match('son') || this.match('daughter') || this.match('father') || this.match('neighbour'))
			return "Dont worry. Just go to the FIR registration page and register your FIR there by giving full details correctly. Upload your signature and Put the OTP that you have received. Your FIR will be registered successfully and investigation panel will come to you for verification. And then you will receive the notifications timely.";
		
		if(this.match('how can i register a new case fir') || this.match('how can i register a new case fir') || this.match('how can i register a new case fir'))
			return "You can register a new case by clicking on new case registration button. Then fill up the details present in it. Upload your signature their and then then fill the OTP that you have received on the registered mobile number.";

		
		if(this.match('is aadhar number required for registration') || this.match('IS Aadhar number required for Registration?') || this.match('is Aadhar number required for Registration'))
			return "Yes, Your Aadhar number is a required field in Registration form.";
		
		if(this.match('is email id required for registration') || this.match('Is Email Id required for Registration?') || this.match('Is Email Id Required for Registration?'))
			return "Yes, Email Id is re required for Registration.";
		
		if(this.match('how can i set my password for registration') || this.match('How can I set my password for Registration?') || this.match('How can I Set my password for Registration?'))
			return "Your password should be between 8 to 15 characters which contain 8 to 15 characters which contain at least one lowercase letter, one uppercase letter, one numeric digit, and one special character.";
		
		if(this.match('how can i get a copy of my fir') || this.match('How can I get a copy of my FIR?') || this.match('How Can I get a copy of my FIR?'))
			return "After Signing In into your account you can click on the option get FIR copy.There you can download your FIR copy.";
		
		if(this.match('how do i get the information about my all registered cases') || this.match('How do I get the information about my all registered cases?') || this.match('How do I get the Information about my all registered cases?'))
			return "After Signing In into your account you can go the view case history page ,you can view all your registered case status.";
		
		if(this.match('which police station will receive my fir') || this.match('Which police Station will receive my Fir?') || this.match('Which police Station will receive my Fir?'))
			return "The nearest police Station according to your location will receive your FIR.";
		
		if(this.match('which option to choose for registering a fir') || this.match('Which option to choose for registering a FIR?') || this.match('Which option to choose for registering a FIR?'))
			return "You need to choose the client option to register a FIR.";
		
		if(this.match('can i lodge a new fir without signing in, in case of emergency') || this.match('Can I Lodge a new FIR without Signing In, in case of emergency?') || this.match('Can I Lodge a new FIR Without Signing In, in case of emergency?'))
			return "No, You can not lodge a FIR without Signing In but you can request for a volunteer.";
		
		if(this.match('what is the requirement of registration') || this.match('What is the requirement of Registration?') || this.match('What is the requirement of Registration?'))
			return "You need to give your Aadhar number, your Email Id, and a valid password to register yourself in to the app.";
		
		if(this.match('who is the client') || this.match('Who is the client?') || this.match('Who is the client?'))
			return "The person who registers  a FIR is called as the client.";
		
		if(this.match('who is sho') || this.match('Who is SHO?') || this.match('Who is SHO?'))
			return "A station house officer (SHO) is the officer in charge of a police station in India and Pakistan. The SHO holds the rank of inspector or sub-inspector. In India, the law permits a station house officer to conduct the investigation of crimes.";
		
		if(this.match('who is sp') || this.match('Who is SP?') || this.match('Who Is SP?'))
			return "Superintendents of police are the officers of either State Police Service or Indian Police Service. They are the district head of non-metropolitan districts in India. They are also the incharge of a large urban or rural area in a district where a senior superintendent is the district head.";
		
		if(this.match('if i forget my password then what should i do') || this.match('If I forget my password then what should I do?') || this.match('If I Forget my password then what should I do?'))
			return "First go the forgot password option.There you need to give your Email Id and then the Link to recover your password will be sent to your Email.";
		
		if(this.match('can i lodge fir for another person') || this.match('Can I lodge FIR for another person?') || this.match('Can I lodge FIR for another person?'))
			return "Yes, You can Register a FIR for another person.";
		
		if(this.match('how can i lodge a fir for another person') || this.match('How can I lodge a FIR for another person?') || this.match('How can I lodge a FIR for another person?'))
			return "You need to click the others button after going to  the FIR registration form page.";
		
		
		
		if(this.match('can i lodge fir for myself') || this.match('Can I lodge FIR for myself?') || this.match('Can I Lodge FIR for myself?'))
			return "Yes, You can Register a FIR for yourself.";
		
		if(this.match('how can i lodge a fir for myself') || this.match('How can I lodge a FIR for myself?') || this.match('How can I lodge a FIR for myself?'))
			return "You need to click the myself button after going to  the FIR registration form page.";
		
		if(this.match('whether i can lodge fir for my relatives only or for any other person') || this.match('Whether I can lodge FIR for my relatives only or for any other person?') || this.match('Whether I can lodge FIR for my relatives only or for any other person?'))
			return "Yes, You can lodge FIR for any person other than your family or relatives.";
		
		
		
		if(this.match('how  can i the lodge fir for any person other than my relatives') || this.match('How  can I the lodge FIR for any person other than my relatives?') || this.match('How  can I the lodge FIR for any person other than my relatives?'))
			return "You can lodge the FIR for any outsider other than your relative by clicking the others button in FIR register form page and then giving the information about how you are related to the person.";
		
		
		if(this.match('what are the mandatory fields while registering fir myself') || this.match('What are the mandatory fields while Registering FIR myself?') || this.match('What are the mandatory fields while Registering FIR myself?'))
			return "While registering  FIR for yourself, Father’s/Husband’s name, City, Police Station, Date, Time and a brief description of the complain fileds are mandatory fields.";
		if(this.match('what are the mandatory fields while registering fir others') || this.match('What are the mandatory fields while Registering FIR others?') || this.match('What are the mandatory fields while Registering FIR others?'))
			return "While registering  FIR for others, Relation,victim’s name,victim’s gender,victim’s age, City, Police Station, Date, Time and a brief description of the complain fileds are mandatory fields.";
		
		if(this.match('is  choosing suspected criminal mandatory') || this.match('Is  choosing suspected criminal mandatory?') || this.match('Is  Choosing suspected criminal mandatory?'))
			return "No, Choosing suspected criminal is an optional field.";
		
		if(this.match('what is sos button used for') || this.match('What is SOS button used for?') || this.match('What Is SOS button used for?'))
			return "SOS button is used as an emergency button.After clicking  the SOS button it will directly lead your emergency  call  to the  Police Station or Hospital.";
		
		
		if(this.match('how to put signature in the signature pad') || this.match('How to put signature in the signature pad?') || this.match('How to put signature in the signature pad?'))
			return "You need to center your phone infront of your face and then give your signature in the signature  pad.";
		
		
		if(this.match('how to find my otp  number') || this.match('How to find my OTP  number?') || this.match('What Does this app doHow to find my OTP  number?'))
			return "OTP(One Time Password) will be sent to your Aadhar registered mobile number.";
		
		
		if(this.match('what should I do if i  did not get my otp number') || this.match('What should I do if I  did not get my OTP number?') || this.match('What should I do if I  did not get my OTP number?'))
			return "Click on the Resend OTP button to resend the OTP number to your aadhar registered mobile number.";
		
		
		if(this.match('how can a sho view his all pending case requests') || this.match('How can a SHO view his all pending case requests?') || this.match('How can a SHO view his all pending case requests?'))
			return "After Singing In into the SHO homepage, SHO can click on the pending requests page to view his all pending case request.";
		if(this.match('what is the role of facilitator') || this.match('What is the role of facilitator?') || this.match('What is the Role of facilitator?'))
			return "A facilitator is a person who helps a group of people to work together better, understand their common objectives, and plan how to achieve these objectives, during meetings or discussions.";
		
		if(this.match('how can a sho learn about his case status') || this.match('How can a SHO learn about his case status?') || this.match('How can a SHO learn about his case status?'))
			return "After Singing In into the SHO homepage, SHO can click on the case records  page to view the status of  all cases.";
		
		
		if(this.match('how can a sp view his new cases ') || this.match('How can a SP view his New cases ?') || this.match('How Can a SP view his New cases ?'))
			return "After Signing In into SP homepage, Click on the New Cases button and it will lead you to the page where the SP can view all the new cases.";
		
		
		if(this.match('how can a sp view his total number of cases ') || this.match('How can a SP View his total number of cases ?') || this.match('How can a SP view his total number of cases ?'))
			return "After Signing In into SP homepage, Click on the FIR RECORD button and it will lead you to the page where the SP can view all the cases.";
		
		
		if(this.match('what is the role of a volunteer') || this.match('What is the role of a volunteer?') || this.match('What is the role of a volunteer?'))
			return "If you have requested for a volunteer then he would arrive to your requested place and help you to lodge the FIR.";
		
		if(this.match('who will accept my fir') || this.match('Who will accept my FIR?') || this.match('Who Will accept my FIR?'))
			return "SHO of the respective police Station will accept or reject  the registered FIR.";
		
		
		if(this.match('how will a fir get rejected') || this.match('How will a FIR get rejected?') || this.match('How will a FIR get rejected?'))
			return "After you register the FIR, SHO has the authority to reject  the FIR.";
		
		
		if(this.match('how will a sho reject  the fir') || this.match('How will a SHO reject  the FIR?') || this.match('How Will a SHO reject  the FIR?'))
			return "SHO has to record his purpose of rejecting the FIR and send it to the complainant.";
		
		
		if(this.match('what  should i do ,if my FIR get rejected by sho') || this.match('What  should I do ,if my FIR get rejected by SHO?') || this.match('What  should I do ,if my FIR get rejected by SHO?'))
			return "You can again register the FIR and send it to the SP.";
		
		
		if(this.match('what is the role an investigation officer') || this.match('What is the role an Investigation Officer?') || this.match('What is the role an Investigation Officer?'))
			return "Investigation officers conduct inquiries to discover who committed crimes and to gather evidence to prosecute and convict suspects. Officers interview suspects and witnesses, examine evidence and conduct research through computer databases and other sources.";
		
		if(this.match('who assigns an investigation officer') || this.match('Who assigns an Investigation Officer?') || this.match('Who Assigns an Investigation Officer?'))
			return "Investigation Officer is normally assigned by the SHO after accepting a registered FIR";
		
		if(this.match('what should i do when i face difficulty in giving the signature in the sign pad') || this.match('What Should I Do when I face difficulty in giving the signature in the sign pad?') || this.match('What should I do when I face difficulty in giving the signature in the sign pad?'))
			return "You can request for a volunteer if you are facing difficulty in giving the signature in the Sign pad.";
		
		if(this.match('which city should i enter while registering a fir') || this.match('Which city should I enter while registering a FIR?') || this.match('Which city should I enter while registering a FIR?'))
			return "You should enter the place where the incident happened only rather than the place where you live.";
		
		if(this.match('which police station should i enter while registering a fir') || this.match('Which police station should I enter while registering a FIR?') || this.match('Which police station should I enter while registering a FIR?'))
			return "You should enter the nearest police station where the incident happened only rather than the nearest police station where you live.";
		
		if(this.match('what time should i enter while registering a fir') || this.match('What Time Should I enter while registering a FIR?') || this.match('What time should I enter while registering a FIR?'))
			return "You should enter the time when the incident happened rather than the time when you are registering the FIR.";
		
		if(this.match('what date should i enter while registering a fir') || this.match('What Date Should I enter while registering a FIR?') || this.match('What date should I enter while registering a FIR?'))
			return "You should enter the date when the incident happened rather than the date when you are registering the FIR.";
		
		if(this.match('What does this app do?') || this.match('what does this app do?') || this.match('What does this app do'))
			return "One can register a FIR report  here without going to the Police Station successfully.";
		
		

		
		
		if(this.match('l(ol)+') || this.match('(ha)+(h|$)') || this.match('lmao'))
			return "what's so funny?";
		
		if(this.match('^no+(\\s|!|\\.|$)'))
			return "don't be such a negative nancy :(";
		
		if(this.match('(cya|bye|see ya|ttyl|talk to you later)'))
			return ["alright, see you around", "good teamwork!"];
		
		if(this.match('(dumb|stupid|is that all)'))
			return ["hey i'm just a proof of concept", "you can make me smarter if you'd like"];
		
		if(this.input == 'noop')
			return;
		
		return input + " what?";
	}
	
	/**
	 * match
	 * 
	 * @param regex - regex string to match
	 * @return boolean - whether or not the input string matches the regex
	 */
	this.match = function(regex) {
	
		return new RegExp(regex).test(this.input);
	}
}
