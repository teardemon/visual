function getJsonFileContent(filePath){
	var FileContent=null;
	$.ajax({
		async:false,
		url : filePath+"?version="+( new Date() ).getTime().toString(),
		success : function(result){
			FileContent=result;
		}
	});
	getFileContent = JSON.parse(FileContent)
	return getFileContent;
}
