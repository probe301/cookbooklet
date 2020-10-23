require(['notebook/js/codecell'], function(codecell) {
  codecell.CodeCell.options_default.highlight_modes['magic_text/x-csharp'] = {'reg':[/^%%csharp/]} ;
  Jupyter.notebook.events.one('kernel_ready.Kernel', function(){
  Jupyter.notebook.get_cells().map(function(cell){
      if (cell.cell_type == 'code'){ cell.auto_highlight(); } }) ;
  });
});

setTimeout(function() {
    Jupyter.keyboard_manager.command_shortcuts.add_shortcut('f5', {
        help : 'run cell',
        handler : function (event) {
            IPython.notebook.execute_cell();
            return false;}});
    Jupyter.keyboard_manager.command_shortcuts.add_shortcut('ctrl-.', {
        help : 'run cell',
        handler : function (event) {
            IPython.notebook.execute_cell();
            return false;}});
    Jupyter.keyboard_manager.edit_shortcuts.add_shortcut('f5', {
        help : 'run cell',
        handler : function (event) {
            IPython.notebook.execute_cell();
            return false;}});
    Jupyter.keyboard_manager.edit_shortcuts.add_shortcut('ctrl-.', {
        help : 'run cell',
        handler : function (event) {
            IPython.notebook.execute_cell();
            return false;}});
    Jupyter.keyboard_manager.edit_shortcuts.add_shortcut('ctrl-enter', {
        help : 'none',
        // 防止与 Sublime hotkey Ctrl+Enter 冲突
        handler : function (event) {
            return false;}});

    Jupyter.keyboard_manager.command_shortcuts.add_shortcut('delete', {
        help : 'none',
        handler : function (event) {
            IPython.notebook.delete_cell();
            return false;}});

    // 设置 python indent 为 2 空格
    var patch = {CodeCell: {cm_config:{indentUnit: 2}}}
    Jupyter.notebook.get_selected_cell().config.update(patch)

    // 依据 ipynb 文件名, 给 cell 加上特定的背景色
    String.prototype.hashCode = function() {
      var hash = 0, i, chr;
      if (this.length === 0) return hash;
      for (i = 0; i < this.length; i++) {
        chr   = this.charCodeAt(i);
        hash  = ((hash << 5) - hash) + chr;
        hash |= 0; // Convert to 32bit integer
      }
      return hash;
    };

    function random_hue_color(label, s, l) {
      // console.log(Math.abs(label.hashCode()))
      var hash_color = (Math.abs(label.hashCode()) % 360) / 360 * 100
      return `hsl(${hash_color}, ${s}%, ${l}%)`
    }

    var notebook_path = IPython.notebook.notebook_path
    var color1 = random_hue_color(notebook_path, 20, 90)
    var color2 = random_hue_color(notebook_path, 40, 80)

    var css = document.createElement("style")
    css.type = "text/css"
    css.innerHTML = `div.cell {background-color: ${color1};}`
    css.innerHTML +=`div.running {background-color: ${color2};}`
    css.innerHTML +=`div.running.selected {background-color: ${color2};}`
    css.innerHTML +=`div.CodeMirror {font-family: "Yahei Mono"; font-size: 20px;}`
    css.innerHTML +='.container { width:100% !important;}'
    css.innerHTML +='.prompt {min-width: 10ex;}'
    css.innerHTML +='.output_text pre, .text_cell_render pre {padding: 0.5ex;}'
    css.innerHTML +='</style>'
    document.body.appendChild(css);

}, 2000)



