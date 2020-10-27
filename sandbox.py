# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 13:45:19 2020

@author: foersterronny
"""
import numpy as np # library for array-manipulation
import matplotlib.pyplot as plt # libraries for plotting
from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import GridSpec
from pdb import set_trace as bp #debugger


## In[]


#here is the file for playing with new functions, debugging and so on


def NewBGFilter(img):
    #checks the background if the histogramm is normal distributed by kolmogorow
    import scipy
    
    img = img / 16
    
    size_y = img.shape[1]
    size_x = img.shape[2]
    
    img_test = np.zeros([size_y,size_x])
    img_mu  = np.zeros([size_y,size_x])
    img_std = np.zeros([size_y,size_x])
    
    for loop_y in range(0, size_y):
        print(loop_y)
        for loop_x in range(0, size_x):
            test = img[: ,loop_y, loop_x]
            mu, std = scipy.stats.norm.fit(test)
            [D_Kolmogorow, _] = scipy.stats.kstest(test, 'norm', args=(mu, std))
    
            img_test[loop_y, loop_x] = D_Kolmogorow
            img_mu[loop_y, loop_x] = mu
            img_std[loop_y, loop_x] = std
    
    return img_test, img_mu, img_std



def TestSlider():
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Slider, Button
    
    x = list(range(0,11))
    y = [10] * 11
    
    fig, ax = plt.subplots()
    plt.subplots_adjust(left = 0.1, bottom = 0.35)
    p, = plt.plot(x,y, linewidth = 2, color = 'blue')
    
    plt.axis([0, 10, 0, 100])
    
    axSlider1 = plt.axes([0.1, 0.2, 0.8, 0.05])
    
    slder1 = Slider()
    
    
    plt.show()



def TryTextBox():
    from matplotlib.widgets import TextBox
    
    fig = plt.figure(figsize = [5, 5], constrained_layout=True)

    gs = GridSpec(2, 1, figure=fig)
    ax_gs = fig.add_subplot(gs[0, 0])
    
    textbox_raw_min = TextBox(ax_gs , "x min: ", initial = "10")    

    ax_plot = fig.add_subplot(gs[1, 0])
    t = np.arange(-2.0, 2.0, 0.001)
    s = t ** 2
    initial_text = "t ** 2"
    l, = ax_plot.plot(t, s, lw=2)


    def PrintASDF(text):
        ax_plot.set_xlim([0.5])
    
    textbox_raw_min.on_submit(PrintASDF)

    return textbox_raw_min


def TryTextBox2():
    #https://matplotlib.org/3.1.1/gallery/widgets/textbox.html
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.widgets import TextBox

    fig = plt.figure(figsize = [5, 5], constrained_layout=True)
    gs = GridSpec(2, 1, figure=fig)
    ax_plot = fig.add_subplot(gs[1, 0])
    
    plt.subplots_adjust(bottom=0.2)
    t = np.arange(-2.0, 2.0, 0.001)
    s = t ** 2
    initial_text = "t ** 2"
    l, = plt.plot(t, s, lw=2)
    
    
    def submit(text):
        t = np.arange(-2.0, 2.0, 0.001)
        print(text)
        ydata = eval(text)
        l.set_ydata(ydata)
        ax_plot.set_ylim(np.min(ydata), np.max(ydata))
        plt.draw()
    
    ax_gs = fig.add_subplot(gs[0, 0])
    textbox_raw_min = TextBox(ax_gs , "x min: ", initial = "10")    
    textbox_raw_min.on_submit(submit)
    
#    axbox = plt.axes([0.1, 0.05, 0.8, 0.075])
#    text_box = TextBox(axbox, 'Evaluate', initial=initial_text)
#    text_box.on_submit(submit)
    
    plt.show()

    return textbox_raw_min



""" 
###############################################################################
Mona's section 
###############################################################################
""" 
    
def DiameterOverTrajLengthColored(ParameterJsonFile, sizes_df_lin, 
                                  color_by='mass', use_log=False,
                                  save_plot = True):
    """ plot (and save) calculated particle diameters vs. the number of frames
    where the individual particle is visible (in standardized format) 
    and color it by a property of choice
    """
        
    import NanoObjectDetection as nd

    settings = nd.handle_data.ReadJson(ParameterJsonFile)
    Histogramm_min_max_auto = settings["Plot"]["Histogramm_min_max_auto"]
    
    if Histogramm_min_max_auto == 1:
        histogramm_min = np.round(np.min(sizes_df_lin.diameter) - 5, -1)
        histogramm_max = np.round(np.max(sizes_df_lin.diameter) + 5, -1)
    else:
        histogramm_min = None
        histogramm_max = None 
    
    histogramm_min, settings = nd.handle_data.SpecificValueOrSettings(histogramm_min, settings, "Plot", "Histogramm_min")
    histogramm_max, settings = nd.handle_data.SpecificValueOrSettings(histogramm_max, settings, "Plot", "Histogramm_max")
    
    my_title = "Particle size over tracking time (colored by {}".format(color_by)
    if use_log==True:
        my_title = my_title + " in log scale)"
    else:
        my_title = my_title + ")"
    my_ylabel = "Diameter [nm]"
    my_xlabel = "Trajectory length [frames]"
    
    plot_diameter = sizes_df_lin["diameter"]
    plot_traj_length = sizes_df_lin["traj length"]
    
    if use_log==True:
        plot_color = np.log10(sizes_df_lin[color_by])
    else:
        plot_color = sizes_df_lin[color_by]
    
    x_min_max = nd.handle_data.Get_min_max_round(plot_traj_length,2)
    x_min_max[0] = 0
    y_min_max = nd.handle_data.Get_min_max_round(plot_diameter,1)
    
    
    plt.figure()
    plt.scatter(plot_traj_length, plot_diameter, c=plot_color, cmap='viridis')
    plt.title(my_title)
    plt.xlabel(my_xlabel)
    plt.ylabel(my_ylabel)
    plt.xlim([x_min_max[0], x_min_max[1]])
    plt.ylim([y_min_max[0], y_min_max[1]])
    plt.colorbar()

 
    if save_plot == True:
        settings = nd.visualize.export(settings["Plot"]["SaveFolder"], "DiameterOverTrajLength",
                                       settings, data = sizes_df_lin)



def AnimateTracksOnRawData(t2_long,rawframes_ROI,settings,frm_start=0):#, gamma=0.5):
    """ animate trajectories on top of raw data
    
    to do:
        - make starting frame free to choose
        - implement gamma transform that does not blow up the file size by a factor of 10!!
        - choose traj. color by length/mass/size/...?
"""
    rawframes_gam = rawframes_ROI.copy()
    # rawframes_gam = 2**16 * (rawframes_gam/2**16)**gamma # for 16bit images
    # rawframes_gam = np.uint16(rawframes_gam)
    
    amnt_f,y_len,x_len = rawframes_ROI.shape
    fps = settings["Exp"]["fps"]
    
    fig,ax = plt.subplots(1,figsize=plt.figaspect(y_len/x_len))
    cm_prism = plt.get_cmap('prism')
    
    # prepare the data
    trajdata = t2_long.copy() 
    trajdata = trajdata.set_index(['frame'])
    trajdata = trajdata.drop(columns=['mass', 'size', 'ecc', 'signal', 'raw_mass', 'ep', 'abstime'])
    
    
    raw_img = ax.imshow(rawframes_gam[0,:,:], cmap='gray', aspect="equal",
                        animated=True)
    # heading = ax.annotate("", (5,10), animated=True,
    #                       bbox=dict(boxstyle="round", fc="white", alpha=0.3, lw=0) )
    # initialize plots for all particles in the whole video
    trajplots = [ax.plot([],[],'-',color=cm_prism(part_id),
                         animated=True
                         )[0] for part_id in trajdata.particle.unique()]
    
    ax.set(xlabel='x [px]', ylabel='y [px]',
           xlim=[0,x_len-1], ylim=[y_len-1,0] ) # invert limits of y-axis!
    # fig.tight_layout() 
    
    def init_tracks():
        raw_img.set_data(rawframes_gam[0,:,:])
        
        for tplot in trajplots:
            tplot.set_data([],[])
        
        # heading.set_text("")
        # ax.set(title='frame: {}, time: {}s'.format(frm_start,time_start))
        # return raw_img, trajplots #,heading
    
    def update_frame(frm): #,trajdata): #,trajplots):
        raw_img.set_data(rawframes_gam[frm,:,:])
        
        # update all trajectory plots individually
        for traj,tplot in zip(trajdata.groupby('particle'),trajplots): 
            # get DataFrame of an individual particle
            _,trajdf = traj # omit the particle ID
            
            # check if current frame adds a trajectory point
            if frm in trajdf.index: 
                tplot.set_data(trajdf.loc[:frm+1].x, trajdf.loc[:frm+1].y)
        
        time = 1000*frm/fps # ms
        # heading.set_text("frame: {}\ntime: {:.1f} ms".format(frm,time))
        ax.set_title("frame: {}, time: {:.1f} ms".format(frm,time))
        
        return raw_img, trajplots#, heading
    
    traj_ani = FuncAnimation(fig, update_frame, init_func=init_tracks, 
                             frames=amnt_f, #fargs=(trajdata),#, trajplots),
                             interval=70, blit=False, repeat=False)
    return traj_ani

# anim2 = AnimateTracksOnRawData(t2_long,rawframes_ROI,settings)
# anim2.save('Au50_raw+tracks_1000frames.mp4')

