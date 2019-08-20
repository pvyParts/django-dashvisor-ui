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

    Supervisor.prototype.do_action = function ($ele, server_alias, action, process) {
        var self = this;
        $.ajax({
            url: this.config.url + server_alias + "/" + process + "/" + action + "/",
            cache: false,
            data: self.config.data || {},
            beforeSend: function (xhr) {
                self.before_action($ele, xhr, action)
            }
        }).done(function (data) {
            self.after_action($ele, data, action);
        }).fail(function (xhr) {
            self.after_action($ele, {}, action);
        })
    };

    Supervisor.prototype.action = function () {
        var self = this;
        self.$ele.each(function () {
            var $ele = $(this);
            var server_alias = $ele.attr("data-server");
            var action = $ele.attr("data-action");
            var process = $ele.attr('data-process');
            $ele.click($.proxy(self.do_action, self, $ele, server_alias, action, process));
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
        if (['start_all', 'stop_all', 'restart_all'].indexOf(action) !== -1) {
            $("button.control-all").attr("disabled", "disabled");
            $ele.find("span.spinner-grow").removeClass('d-none');
        }
    };

    Supervisor.prototype.after_command = function ($ele, xhr, action) {
        if (['start_all', 'stop_all', 'restart_all'].indexOf(action) !== -1) {
            setTimeout(function () {
                $ele.find("span.spinner-grow").addClass('d-none');
                $("button.control-all").removeAttr("disabled");
            }, parseInt($.urlParam('autorefresh', 5)) * 1000)
        }
    };

    Supervisor.prototype.before_tail = function ($ele, xhr) {
        if (!$ele.data("setTimeoutHandler")) {
            var $modal_body = this.config.screen.find(".modal-body");
            $modal_body.find(".loading").removeClass("d-none");
            $modal_body.find(".content").empty();
            this.config.screen.find('.modal-title')
                .text("Tail " + $ele.text() + " stdout");
            this.config.screen.modal("show");
            this.config.screen.on('hide.bs.modal', function () {
                clearTimeout($ele.data("setTimeoutHandler"));
                $ele.removeData("setTimeoutHandler");
            });
        }
    };

    Supervisor.prototype.after_tail = function ($ele, data) {
        var $modal_body = this.config.screen.find(".modal-body");
        var result = data.result;
        if (result) {
            if (result.content.length > 0) {
                $modal_body.find(".loading").addClass("d-none");
                $modal_body.find(".content").append(result.content);
            }
            this.config.data.offset = result.size;
        }
        var server = $ele.attr("data-server");
        var action = $ele.attr("data-action");
        var process = $ele.attr('data-process');

        $ele.data("setTimeoutHandler", setTimeout($.proxy(this.do_action, this),
            this.config.screen_update, $ele, server, action, process));
    };

    Supervisor.prototype.before_action = function ($ele, xhr, action) {
        if (action === 'tail') {
            this.before_tail($ele, xhr);
        } else {
            this.before_command($ele, xhr, action);
        }
    };

    Supervisor.prototype.after_action = function ($ele, data, action) {
        if (action === 'tail') {
            this.after_tail($ele, data);
        } else {
            this.after_command($ele, data, action);
        }
    };

    $.fn.Supervisor = Supervisor;
    $.fn.supervisor = function (config) {
        return new Supervisor($(this), config || {})
    };

}(jQuery));