import numpy as np

COLOURS = ['black', 'blue', 'm', 'sienna', 'cyan', 'red', 'orange', 'green', '#0F95D7', 'lawngreen',
           'gold', 'violet', 'indigo', 'cornflowerblue', 'orangered', 'darkslategrey', 'black', 'fuchsia', 'olive']
MARKERS = ['', 'o', 's', 'd', 'x', '^', 'p', '.', '+', '*']
LINE_STYLES = ['-', '--', '-.', ':', (0, (1, 10)), (0, (1, 5)), (0, (1, 1)), (5, (10, 3))]


def load_numpy_with_header(filepath):
    with open(filepath) as f:
        header = f.readline().lstrip("#").strip()
        header = header.split(',') if ',' in header else header.split()

    data = np.genfromtxt(filepath, skip_header=True)

    return data, header


def set_default_mpl_formatting(linewidth=1.75, fontsize=20, fontsize_legend=16, font_family='Gulliver-Regular', font_paths=None):
    # Matplotlib Formatting
    import matplotlib as mpl
    mpl.font_manager._get_fontconfig_fonts.cache_clear()
    font_files = mpl.font_manager.findSystemFonts(fontpaths=font_paths,
                                                  fontext='ttf')
    for font in font_files:
        if font_family in font:
            mpl.font_manager.fontManager.addfont(font)

    from pathlib import Path

    current_file_path = Path(__file__).resolve()
    # Get the parent directory
    font_path = current_file_path.parent / './fonts/'

    # font_path = os.getcwd()
    font_files = mpl.font_manager.findSystemFonts(fontpaths=str(font_path))

    for font_file in font_files:
        mpl.font_manager.fontManager.addfont(font_file)

    mpl.rc('font', family=font_family)
    mpl_font = {'fontname': font_family}
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['ps.fonttype'] = 42
    mpl.rcParams['font.family'] = font_family
    mpl.rc('axes', linewidth=linewidth, labelsize=fontsize, titlesize=fontsize)
    mpl.rc('xtick', labelsize=fontsize)
    mpl.rc('ytick', labelsize=fontsize)
    mpl.rc('legend', fontsize=fontsize_legend)
    mpl.rcParams.update({'font.size': fontsize})
