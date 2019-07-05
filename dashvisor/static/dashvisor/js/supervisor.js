(function ($) {

    var Supervisor = function ($ele, config) {
        this.$ele = $ele;
        this.config = config;
    };

    Supervisor.prototype.action = function () {
        var self = this;
        var server = this.$ele.attr("data-server");
        var action = this.$ele.attr("data-action");
        var process = this.$ele.attr('data-process');
        this.$ele.click(function () {
            $.ajax({
                url: self.config.url + server + "/" + process + "/" + action + "/",
                cache: false,
                beforeSend: function (xhr) {
                    self.before_action(xhr, action)
                }
            }).done(function (data) {
                self.after_action(data, action);
            })
        })
    };
    Supervisor.prototype.before_action = function (xhr, action) {

    };

    Supervisor.prototype.after_action = function (data, action) {

    };

    $.fn.supervisor = function (config) {
        return this.each(function () {
            var supervisor = new Supervisor($(this), config || {});
            $.proxy(supervisor.action, supervisor)();
        });
    };

}(jQuery));