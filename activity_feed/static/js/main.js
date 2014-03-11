// jQuery IIFE
// source: http://gregfranko.com/blog/i-love-my-iife/
(function(jscode) {
    jscode(window.jQuery, window, document);
}(function($, window, document) {
    $(function() {

        // The DOM is ready

        var add_activity = $('#add_activity');
        var activity_list = $('#activity_list');
        var content = add_activity.find('#activity_content');
        var category_select = add_activity.find('#category');
        var filter = $('#filter');
        var creator_filter = filter.find('#creator_filter');
        var target_filter = filter.find('#target_filter');


        // set default values on page refresh
        $(window).load(function() {
            // unnecessary elements
            filter.find('input[type=submit]').remove();      // filter button
            activity_list.find('#pagination').remove();      // paginator

            category_select[0].selectedIndex = 0;  // first list element
            category_select.trigger('change');

            creator_filter.val('');
            target_filter.val('');
            filter.find('select').trigger('change');
            });


        // show custom content text area
        category_select.change(function() {
            if ($(this).val() == '') {  // selected custom content
                content.show();
                }
            else {
                content.hide();
                }
            }).change();

        // filter activities
        filter.change('select', function() {
            var creator_id = creator_filter.val();
            var target_id = target_filter.val();
            filterBy(creator_id, target_id).done(function(data) {
                activity_list.html(data);
                });
            }).change();

        // add activity
        add_activity.submit(function(e) {
            var creator_id = creator_filter.val();
            var target_id = target_filter.val();
            var form = $(this).find('form');
            var new_creator = form.find('#new_creator');
            var new_target = form.find('#new_target');

            e.preventDefault();  // cancel form submit request

            addActivity(form).done(function(data) {
                if (((new_creator.val() == creator_id) || (creator_id == '')) &&
                    ((new_target.val() == target_id) || (target_id == '')) &&
                    (data != '')) {

                    activity_list.prepend(data);  // new activity on top
                    }
                data = '';  // clear data
                });
            });

        });


    // The DOM is not ready

    function filterBy(creator_id, target_id) {
        /*
        Sends ajax request to filter activities
        */
        var uri = '/';
        if (creator_id != '') {
            uri += 'creator/' + creator_id + '/';
            }
        if (target_id != '') {
            uri += 'target/' + target_id + '/';
            }

        return $.ajax(uri);
        };


    function addActivity(form) {
        /*
        Sends ajax request to create new activity.
        */
        var formData = form.serialize();

        return $.post('/new/', formData, 'html');
        };

}));
