function DOMTemplateEngine(base) {
    // configuration
    this.base = base;
}

DOMTemplateEngine.prototype.getSource = function (name) {
    // load the template
    // return an object with:
    //   - src:     String. The template source.
    //   - path:    String. Path to template.
    //   - noCache: Bool. Don't cache the template (optional).
    var path = this.base + '-' + name;
    return {
        src: $(path).text(),
        path: path,
        noCache: true
    }
};