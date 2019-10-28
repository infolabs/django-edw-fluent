CKEDITOR.plugins.add( 'hottag', {
    icons: 'hottag',
    init: function( editor ) {
        editor.addCommand( 'hottag', new CKEDITOR.dialogCommand( 'hottagDialog' ) );
        editor.ui.addButton( 'Hottag', {
            label: 'Insert Hottag',
            command: 'hottag',
            toolbar: 'insert'
        });
        CKEDITOR.dialog.add( 'hottagDialog', this.path + 'dialogs/hottag.js' );
    }
});