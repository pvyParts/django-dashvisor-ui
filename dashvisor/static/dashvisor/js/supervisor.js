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
                cache: false
            }).done(function (data) {
                self['on_' + action](data);
            })
        })
    };

    Supervisor.prototype.on_start = function (data) {

    };

    Supervisor.prototype.on_stop = function (data) {

    };

    Supervisor.prototype.on_restart = function (data) {
    };

    $.fn.supervisor = function (config) {
        return new Supervisor(this, config || {});
    };

}(jQuery));