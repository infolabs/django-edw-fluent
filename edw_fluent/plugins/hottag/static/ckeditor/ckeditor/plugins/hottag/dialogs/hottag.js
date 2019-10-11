
function ge_search_data(str) {
	var search_url = '/hottagplugin/hottagsearch/';
	var res = $.ajax({
		url: search_url,
		async: false,
        cache: false,
        timeout: 10000,
		data: {'q': str}
	}).done(function (resp) {

		return resp;
	}).error(function (resp) {

		return {};
	});

	if (res && res.responseJSON){
		return res.responseJSON;
	}else{
		return {};
	}
	return {};
}

CKEDITOR.dialog.add( 'hottagDialog', function( editor ) {
    return {
        //allowedContent: "a[href,target]", 
		title: "Add hot tag",
		minWidth: 550, 
		minHeight: 100, 
		resizable: CKEDITOR.DIALOG_RESIZE_NONE,
		 contents:[{
			 id: "HotTag",
			 label: "HotTag",
			 elements:[
				 {
					 type: "text", 
					 label: "Тег",
					 id: "edw-tag", 
					 setup: function( element ) { 
						 var tag = element.getAttribute("data-edw-tag");

						 if(tag == "" || tag == null){
							 tag = element.getText();

						 }

						 this.setValue(tag); 
					 },
					 commit: function(element) {
						 var currentValue = this.getValue();
						 if(currentValue !== "" && currentValue !== null) { 
							 element.setAttribute("data-edw-tag", currentValue);
						 } 
					 }
			 	},
				 {
						type: 'button',
						id: 'edw-search',
						label: 'Найти публикацию по тегу',
						title: 'Поиск',
						onClick: function() {
							var dialog = this.getDialog();
							var edw_tag = dialog.getContentElement("HotTag",'edw-tag');//.getElement();
							var tag = edw_tag.getValue();
							var query_data = ge_search_data(tag);

							if (tag!=""){
								dialog.element.setAttribute("data-edw-tag", tag);
							} else {
								dialog.element.removeAttribute("data-edw-tag");
							};

							if (query_data.hasOwnProperty('model_id')){
								dialog.element.setAttribute("data-edw-model-id", query_data['model_id']);
							} else {
								dialog.element.removeAttribute('data-edw-model-id');
							};

							if (query_data.hasOwnProperty('title')){
								dialog.element.setAttribute("title", query_data['title']);
							} else {
								dialog.element.removeAttribute("title");
							};

							if (query_data.hasOwnProperty('url')){
								dialog.element.setAttribute("href", query_data['url']);
							}else {
								dialog.element.removeAttribute("href");
							};

							// update preview
							var eHtml = dialog.getContentElement("HotTag",'edw-link').getElement();
							var tile = dialog.element.getAttribute("title");
							var href = dialog.element.getAttribute("href");
							if (tile && href){
								 eHtml.setHtml('<h4>Текущая публикация:</h4><a target="_blank" style="color:#447e9b; text-decoration: underline;" href="' + href +'">'+tile+'</a>');
							}else{
								eHtml.setHtml("<h4>Нет подходящих публикаций</h4>" );
							};

							}
					},
				 {
					 type: "text",
					 label: "Заголовок",
					 id: "edw-text",
					 validate: CKEDITOR.dialog.validate.notEmpty( "Text cannot be empty." ),
					 setup: function( element ) {
						 var text = element.getText();
						 if(text) {
							 this.setValue(text);
						 }
					 },
					 commit: function(element) { 
						 var text = this.getValue();
						 if(text) {
							 element.setText(text);
						 }
					 }
				 }, 
				 { 
					 type: "html",
					 id: "edw-link",
					 html: "<h4>Нет подходящих публикаций</h4>" , 

				 }

			 ] 
		 }]
		, onShow: function() {
			var selection = editor.getSelection();
			var selector = selection.getStartElement()
			var element;

			if(selector) {
				element = selector.getAscendant( 'a', true );
			} 
			if ( !element || element.getName() != 'a' ) {
				element = editor.document.createElement( 'a' ); 

				if(selection) { 
					element.setText(selection.getSelectedText()); 
				}
				this.insertMode = true; 
			} else{
				this.insertMode = false;
			}

			var c_txt = element.getAttribute("data-edw-tag") || element.getText()

			if ( !element.getAttribute("data-edw-model-id") && c_txt){
				var query_data = ge_search_data(c_txt);

				if (query_data){
					if (query_data.hasOwnProperty('model_id')){
						element.setAttribute("data-edw-model-id", query_data['model_id']);
					};
					if (query_data.hasOwnProperty('title')){
						element.setAttribute("title", query_data['title']);
					};
					if (query_data.hasOwnProperty('url')){
						element.setAttribute("href", query_data['url']);
					};
				}
			}

			element.addClass( 'edw-hottag' );
			this.element = element; 
			eHtml = this.getContentElement("HotTag",'edw-link').getElement();
          	var tile = element.getAttribute("title");
			var href = element.getAttribute("href");

			if (tile && href && href!="#"){
				 eHtml.setHtml('<h4>Текущая публикация:</h4><a target="_blank" style="color:#447e9b; text-decoration: underline;" href="' + href +'">'+tile+'</a>');
			}

			this.setupContent(this.element); 
		}
		, onOk: function() { 
			var dialog = this; 
			var anchorElement = this.element; 
			this.commitContent(this.element);
			if(this.insertMode) {
				editor.insertElement(this.element); 
			} ;

		}

    };
});