function add_tag(tag)
{
	var obj = document.getElementById("editbox");
	var temp = obj.value;
	obj.value = temp.substring(0, obj.selectionStart) + tag + temp.substring(obj.selectionEnd, temp.length); 
}

function add_img()
{
	var tag = '<div class="img"><img src="" alt=""></div>';
	add_tag(tag);
}

function add_url()
{
	var tag = '<a href=""></a>';
	add_tag(tag);
}

function add_strong()
{
	var tag = '<span style="color:red;"></span>';
	add_tag(tag);
}

function add_em()
{
	var tag = '<span style="font:bold;"></span>';
	add_tag(tag);
}	

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
