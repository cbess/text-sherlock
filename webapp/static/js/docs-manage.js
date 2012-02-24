/**
 * Provides clients side logic for the doc management pages
 */

var TSDocManage = {
    // handles page loading
    onPageLoad: function()
    {
        // add project document
        $('#projects form button[name="btn_add_file"]').click(function() {
            var pname = $(this).parent('form').data('project-name');
            return confirm('Add the files to '+pname+'?');
        });
        
        // delete project action
        $('#projects form button[name="btn_delete_proj"]').click(function() {
            var pname = $(this).parent('form').data('project-name');
            return confirm('Delete "'+pname+'" and all it\'s files? This cannot be undone.');
        });
        
        // delete project document action
        $('#projects form button[name="btn_delete_file"]').click(function() {
            var form = $(this).parents('form');
            var pname = form.data('project-name');
            var fname = $(this).data('filename');
            return confirm('Delete "'+fname+'" from '+pname+'? This cannot be undone.');
        });
    }
};

$(function() {
    TSDocManage.onPageLoad();
});