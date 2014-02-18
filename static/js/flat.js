function getClass()
{
	var rs = []; 
	var all_tag = document.all;
	for(var i = 0; i < all_tag.length; i++){
		var flag = true;
		var classes = all_tag[i].className.split(/\s+/);
		var h = [];
		for(var j = 0; j < classes.length; j++){
			h[classes[j]] = classes[j];	
		}
		for(var j = 0; j < arguments.length; j++){
			if(h[arguments[j]] == undefined){
				flag = false;
			}
		}
		if(flag){
			rs[rs.length] = all_tag[i];
		}
	}
	return rs;
}

function input_text_focus(obj)
{
	if(obj.value == obj.defaultValue){
		obj.value = "";	
		obj.style.color = "#000";
	}
	console.log("call input_text_focus");
}

function input_text_blur(obj, value)
{
	if(obj.value == ""){
		obj.value = obj.defaultValue;
		obj.style.color = "#666";
	}
	console.log("call input_text_blur");
}

function evt_handler()
{
	var e = getClass("text", "default");
	for(var i = 0; i < e.length; i++){
		e[i].onfocus = function(){
			input_text_focus(this);
		}
		e[i].onblur = function(){
			input_text_blur(this);	
		}
	}
}

evt_handler();
