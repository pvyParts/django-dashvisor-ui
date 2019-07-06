(function ($) {

    var Supervisor = function ($ele, config) {
        this.$ele = $ele;
        this.config = config;
    };

    Supervisor.prototype.action = function () {
        var self = this;
        self.$ele.each(function () {
            var $ele = $(this);
            var server = $ele.attr("data-server");
            var action = $ele.attr("data-action");
            var process = $ele.attr('data-process');
            $ele.click(function () {
                $.ajax({
                    url: self.config.url + server + "/" + process + "/" + action + "/",
                    cache: false,
                    beforeSend: function (xhr) {
                        self.before_action($ele, xhr, action)
                    }
                }).done(function (data) {
                    self.after_action($ele, data, action);
                })
            });
        });
        return this;
    };


    Supervisor.prototype.before_command = function ($ele, xhr, action) {
        $ele.attr("disabled", "disabled");
    };

    Supervisor.prototype.after_command = function ($ele, xhr, action) {
        $ele.removeAttr("disabled")
    };

    Supervisor.prototype.before_tail = function ($ele, xhr) {
        this.config.screen.find(".modal-body").empty();
        this.config.screen.modal("show");
    };

    Supervisor.prototype.after_tail = function ($ele, data) {
        this.config.screen.find(".modal-body").html("<pre>" + data.result[0] + "</pre>");
    };

    Supervisor.prototype.before_action = function ($ele, xhr, action) {
        if (['start', 'stop', 'restart'].indexOf(action) !== -1) {
            this.before_command($ele, xhr, action);
        } else if (action === 'tail') {
            this.before_tail($ele, xhr);
        }
    };

    Supervisor.prototype.after_action = function ($ele, data, action) {
        if (['start', 'stop', 'restart'].indexOf(action) !== -1) {
            this.after_command($ele, data, action);
        } else if (action === 'tail') {
            this.after_tail($ele, data);
        }
    };

    $.fn.supervisor = function (config) {
        return new Supervisor($(this), config || {})
    };

}(jQuery));