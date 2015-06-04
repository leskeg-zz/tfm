# -*- coding: utf-8 -*-
import mpld3

class TopToolbar(mpld3.plugins.PluginBase):
    """Plugin for moving toolbar to top of figure"""

    JAVASCRIPT = """
    mpld3.register_plugin("toptoolbar", TopToolbar);
    TopToolbar.prototype = Object.create(mpld3.Plugin.prototype);
    TopToolbar.prototype.constructor = TopToolbar;
    function TopToolbar(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    TopToolbar.prototype.draw = function(){
      // the toolbar svg doesn't exist
      // yet, so first draw it
      this.fig.toolbar.draw();

      // then change the y position to be
      // at the top of the figure
      this.fig.toolbar.toolbar.attr("x", 150);
      this.fig.toolbar.toolbar.attr("y", 400);

      // then remove the draw function,
      // so that it is not called again
      this.fig.toolbar.draw = function() {}
    }
    """
    def __init__(self):
        self.dict_ = {"type": "toptoolbar"}

#define custom css to format the font and to remove the axis labeling
css = """
text.mpld3-text, div.mpld3-tooltip {
  font-family:Arial, Helvetica, sans-serif;
}

g.mpld3-xaxis, g.mpld3-yaxis {
display: none; }

svg.mpld3-figure {
margin-left: -100px;}
"""

#iterate through groups to layer the plot
#note that I use the cluster_name and cluster_color dicts with the 'name' lookup to return the appropriate color/label
def plot(groups,fig,ax,cluster_names,cluster_colors):
	for name, group in groups:
	    points = ax.plot(group.x, group.y, marker='o', linestyle='', ms=18, 
	                     label=cluster_names[name], mec='none', 
	                     color=cluster_colors[name])
	    ax.set_aspect('auto')
	    labels = [i for i in group.title]
	    
	    #set tooltip using points, labels and the already defined 'css'
	    tooltip = mpld3.plugins.PointHTMLTooltip(points[0], labels,
	                                       voffset=10, hoffset=10, css=css)
	    #connect tooltip to fig
	    mpld3.plugins.connect(fig, tooltip, TopToolbar())    
	    
	    #set tick marks as blank
	    ax.axes.get_xaxis().set_ticks([])
	    ax.axes.get_yaxis().set_ticks([])
	    
	    #set axis as blank
	    ax.axes.get_xaxis().set_visible(False)
	    ax.axes.get_yaxis().set_visible(False)

	    
	ax.legend(numpoints=1) #show legend with only one dot
	file_ = open('clustering.html', 'w')
	file_.write(mpld3.fig_to_html(fig))
	file_.close()
	mpld3.show() #show the plot