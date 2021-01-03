$(document).ready(function() {
			$('#modal').modal('show');

			$('#signArea').signaturePad({drawOnly:true, drawBezierCurves:true, lineTop:90, lineWidth:0});

			$('#btnClearSign').click(function(e){
    			$('#signArea').signaturePad().clearCanvas();
   			});

//   			$('#btnSubmitSign').click(function (event) {
//   					var canvas = document.getElementById("sign-pad");
//    				var dataURL = canvas.toDataURL();
////    				download(dataURL, "signature.png");
//
//			});

			setTimeout(function(){$('#modal').modal('hide')},5000);
				
			});
			
			
//				function download(dataURL, filename) {
//  					var blob = dataURLToBlob(dataURL);
//  					var url = window.URL.createObjectURL(blob);
//
//  					var a = document.createElement("a");
//  					a.style = "display: none";
// 					a.href = url;
//  					a.download = filename;
//
//  					document.body.appendChild(a);
//  					a.click();
//
//  					window.URL.revokeObjectURL(url);
//				}
				function dataURLToBlob(dataURL) {
  				// Code taken from https://github.com/ebidel/filer.js
  					var parts = dataURL.split(';base64,');
  					var contentType = parts[0].split(":")[1];
  					var raw = window.atob(parts[1]);
  					var rawLength = raw.length;
  					var uInt8Array = new Uint8Array(rawLength);

  					for (var i = 0; i < rawLength; ++i) {
    					uInt8Array[i] = raw.charCodeAt(i);
  					}

  					return new Blob([uInt8Array], { type: contentType });
				}

			
			window.onload = function(){
				init();
				window.addEventListener('resize', init, false);
			}
			function init(){
				var pad = document.getElementById('sign-pad');
				var context = pad.getContext('2d');
				var myWidth = window.innerWidth -90;
				var myHeight = window.innerHeight -250;
				context.canvas.width = myWidth;
				context.canvas.height = myHeight;
			}