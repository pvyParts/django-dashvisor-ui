(function ($) {
    $.urlParam = function (name, _default) {
        var results = new RegExp('[\\?&]' + name + '=([^&#]*)').exec(window.location.href);
        return (results && results[1]) || _default || 0;
    };

    var Supervisor = function ($ele, config) {
        this.$ele = $ele;
        this.config = config;
        $.extend(this.config, {screen_update: 5000})
    };

    Supervisor.prototype.do_action = function ($ele, server, action, process) {
        var self = this;
        $.ajax({
            url: this.config.url + server + "/" + process + "/" + action + "/",
            cache: false,
            beforeSend: function (xhr) {
                self.before_action($ele, xhr, action)
            }
        }).done(function (data) {
            self.after_action($ele, data, action);
        })
    };

    Supervisor.prototype.action = function () {
        var self = this;
        self.$ele.each(function () {
            var $ele = $(this);
            var server = $ele.attr("data-server");
            var action = $ele.attr("data-action");
            var process = $ele.attr('data-process');
            $ele.click($.proxy(self.do_action, self, $ele, server, action, process));
        });
        return this;
    };

    Supervisor.isRunningState = function(state) {
        return ['starting', 'running'].indexOf(state.toLowerCase()) !== -1;
    };

    Supervisor.isStoppedState = function(state) {
        return ['stopped', 'starting'].indexOf(state.toLowerCase()) !== -1;
    };

    Supervisor.prototype.before_command = function ($ele, xhr, action) {
        $ele.attr("disabled", "disabled");
    };

    Supervisor.prototype.after_command = function ($ele, xhr, action) {};

    Supervisor.prototype.before_tail = function ($ele, xhr) {
        if (!$ele.data("setIntervalID")) {
            this.config.screen.find(".modal-body").html(
                '<div class="d-flex justify-content-center">' +
                '<button class="btn btn-light" type="button" disabled>' +
                '  <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>' +
                '  Loading...' +
                '</button>' +
                '</div>');

            this.config.screen.modal("show");
            this.config.screen.find('.modal-title')
                .text("Tail " + $ele.text() + " stdout");

            var server = $ele.attr("data-server");
            var action = $ele.attr("data-action");
            var process = $ele.attr('data-process');

            $ele.data("setIntervalID",
                setInterval($.proxy(this.do_action, this),
                    this.config.screen_update, $ele, server, action, process));

            this.config.screen.on('hide.bs.modal', function () {
                clearInterval($ele.data("setIntervalID"));
                clearInterval($ele.removeData("setIntervalID"))
            })
        }
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

    $.fn.Supervisor = Supervisor;
    $.fn.supervisor = function (config) {
        return new Supervisor($(this), config || {})
    };

}(jQuery));