(function ($) {

    var Supervisor = function ($ele, config) {
        this.$ele = $ele;
        this.config = config;
    };

    Supervisor.prototype.action = function () {
        var self = this;
        self.$ele.each(function () {
            var $btn = $(this);
            var server = $btn.attr("data-server");
            var action = $btn.attr("data-action");
            var process = $btn.attr('data-process');
            $btn.click(function () {
                $.ajax({
                    url: self.config.url + server + "/" + process + "/" + action + "/",
                    cache: false,
                    beforeSend: function (xhr) {
                        self.before_action($btn, xhr, action)
                    }
                }).done(function (data) {
                    self.after_action($btn, data, action);
                })
            });
        });
        return this;
    };

    Supervisor.prototype.before_action = function ($ele, xhr, action) {
        $ele.attr("disabled", "disabled")
    };

    Supervisor.prototype.after_action = function ($ele, data, action) {
        $ele.removeAttr("disabled")
    };

    $.fn.supervisor = function (config) {
        return new Supervisor($(this), config || {})
    };

}(jQuery));