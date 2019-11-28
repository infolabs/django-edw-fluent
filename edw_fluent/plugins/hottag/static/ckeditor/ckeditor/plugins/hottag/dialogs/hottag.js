
function ge_search_data(str, publication_id) {

	var search_url = '/hottagplugin/hottagsearch/';
	var res = $.ajax({
		url: search_url,
		async: false,
        cache: false,
        timeout: 10000,
		data: {'q': str, 'pid': publication_id}
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
					 validate: CKEDITOR.dialog.validate.notEmpty( "Тег не может быть пустым" ),
					 id: "edw-tag", 
					 setup: function( dialog ) { 
						 this.setValue(dialog.data_edw_tag_txt); 
					 },
					 commit: function(dialog) {
						 var currentValue = this.getValue();

						 dialog.data_edw_tag_txt = currentValue;
						  
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
							var query_data = ge_search_data(tag, dialog.publication_id);

							dialog.data_edw_tag_txt = tag;

							if (query_data.hasOwnProperty('model_id')){
								dialog.data_edw_model_id = query_data['model_id'];
							} else {
								dialog.data_edw_model_id = "";
							};

							if (query_data.hasOwnProperty('title')){
								dialog.data_edw_title = query_data['title'];
							} else {
								dialog.data_edw_title = "";
							};

							if (query_data.hasOwnProperty('url')){
								dialog.data_edw_href = query_data['url'];
							}else {
								dialog.data_edw_href = "";
							};

							// update preview
							var eHtml = dialog.getContentElement("HotTag",'edw-link').getElement();


							if (dialog.data_edw_title && dialog.data_edw_href){
								 eHtml.setHtml('<h4>Текущая публикация:</h4><a target="_blank" style="color:#447e9b; text-decoration: underline;" href="' + dialog.data_edw_href +'">'+dialog.data_edw_title+'</a>');
							}else{
								eHtml.setHtml("<h4>Нет подходящих публикаций</h4>" );
							};

							}
					},
				 {
					 type: "text",
					 label: "Заголовок",
					 id: "edw-text",
					 validate: CKEDITOR.dialog.validate.notEmpty( "Заголовок не может быть пустым" ),
					 setup: function( dialog ) {
						 this.setValue(dialog.data_edw_selection_txt);

					 },
					 commit: function(dialog) {
						 var currentValue = this.getValue();

						 dialog.data_edw_selection_txt = currentValue;
						  
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
			var selector = selection.getStartElement();
			var element;
			var data_edw_id;
			var data_edw_tag_txt;
			var data_edw_selection_txt;
			var data_edw_model_id;
			var data_edw_title;
			var data_edw_href;
			var href = document.location.href;
			var re_id = href.match(/\/(\d+)\//);
			var publication_id =  re_id ? re_id[1] : null;

			this.publication_id = publication_id;



			if(selector) {
				element = selector.getAscendant( 'a', true );
				if (!element){
					element = selector.getAscendant( 'span', true );
				}
			} 

			this.element = element;


			if (element){
				data_edw_id = element.getAttribute("data_edw_id");
				data_edw_tag_txt = element.getAttribute("data-edw-tag") || element.getText();
				data_edw_selection_txt = element.getText();
				data_edw_model_id = element.getAttribute("data-edw-model-id");
				data_edw_title = element.getAttribute("title");
				data_edw_href = element.getAttribute("href");
			}else{
				data_edw_id = null;
				if(selection) { 
					data_edw_tag_txt = selection.getSelectedText();
					data_edw_selection_txt = selection.getSelectedText();
				}else{
					data_edw_tag_txt = "";
					data_edw_selection_txt = "";
				}
			}

			if ( !data_edw_model_id && data_edw_tag_txt){
				var query_data = ge_search_data(data_edw_tag_txt, this.publication_id);

				if (query_data){
					if (query_data.hasOwnProperty('model_id')){
						data_edw_model_id = query_data['model_id'];
					}else{
						data_edw_model_id = "";
					}
					if (query_data.hasOwnProperty('title')){
						data_edw_title = query_data['title'];
					}else {
						data_edw_title = "";
					}
					if (query_data.hasOwnProperty('url')){
						data_edw_href = query_data['url'];
					}else {
						data_edw_href = "";
					}
				}
			}


			eHtml = this.getContentElement("HotTag",'edw-link').getElement();

			if (data_edw_title && data_edw_href){
				 eHtml.setHtml('<h4>Текущая публикация:</h4><a target="_blank" style="color:#447e9b; text-decoration: underline;" href="' + data_edw_href +'">'+data_edw_title+'</a>');
			}else{
				eHtml.setHtml("<h4>Нет подходящих публикаций</h4>" );
			};

			this.data_edw_tag_txt = data_edw_tag_txt;
			this.data_edw_model_id = data_edw_model_id;
			this.data_edw_title = data_edw_title;
			this.data_edw_href = data_edw_href;
			this.data_edw_selection_txt = data_edw_selection_txt;
			this.data_edw_id = data_edw_id;



			this.setupContent(this);  //dialog
		}
		, onOk: function() { 
			var dialog = this; 
			var anchorElement = this.element; 
			this.commitContent(dialog);

			if (this.data_edw_tag_txt && this.data_edw_tag_txt!=""){
				var query_data = ge_search_data(this.data_edw_tag_txt, this.publication_id);

				if (query_data.hasOwnProperty('model_id')){
					dialog.data_edw_model_id = query_data['model_id'];
				} else {
					dialog.data_edw_model_id = "";
				};

				if (query_data.hasOwnProperty('title')){
					dialog.data_edw_title = query_data['title'];
				} else {
					dialog.data_edw_title = "";
				};

				if (query_data.hasOwnProperty('url')){
					dialog.data_edw_href = query_data['url'];
				}else {
					dialog.data_edw_href = "";
				};

			}else{

				this.data_edw_href = "";
				this.data_edw_title = "";
				this.data_edw_model_id = "";

			};

			if(anchorElement){
				this.insertMode = false;
				if (this.data_edw_href && this.data_edw_href!="") {
					//<a> tag
					if(anchorElement.getName() != 'a'){
						anchorElement.renameNode('a');
					};
				}else{
					// span tag
					if(anchorElement.getName() != 'span'){
						anchorElement.renameNode('span');
					};
				}

			}else{

				this.insertMode = true;
				if (this.data_edw_href && this.data_edw_href!="") {
					anchorElement = editor.document.createElement('a');
				}else{
					anchorElement = editor.document.createElement('span');
				}
			};


			if (this.data_edw_selection_txt){
				anchorElement.setText(this.data_edw_selection_txt);
			};

			if (this.data_edw_tag_txt && this.data_edw_tag_txt!=""){
				anchorElement.setAttribute("data-edw-tag", this.data_edw_tag_txt);
			} else {
				anchorElement.removeAttribute("data-edw-tag");
			};


			if (this.data_edw_title && this.data_edw_title!=""){
				anchorElement.setAttribute("title", this.data_edw_title);
			} else {
				anchorElement.removeAttribute("title");
			};


			if (this.data_edw_model_id && this.data_edw_model_id!="" ){
				anchorElement.setAttribute("data-edw-model-id", this.data_edw_model_id);
			} else {
				anchorElement.removeAttribute("data-edw-model-id");
			};


			if (this.data_edw_href && this.data_edw_href!="" ){
				anchorElement.setAttribute("href", this.data_edw_href);
			} else {
				anchorElement.removeAttribute("href");
			};


			anchorElement.addClass('edw-hottag');
			this.element = anchorElement;

			if(this.insertMode) {
				editor.insertElement(this.element); 
			} ;

		}

    };
});