import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path

from utils import load_numpy_with_header, set_default_mpl_formatting, COLOURS, MARKERS, LINE_STYLES

figsize = (9, 7)
fontsize = 22
linewidth = 2
set_default_mpl_formatting(fontsize=fontsize, linewidth=linewidth)


alpha_bounds = {
    'nt': (-5., 12.5),
    'ng': (-5., 12.5),
}

cl_cd_bounds = {
    'nt': {'x': (None, 0.15), 'y': (None, None)},
    'ng': {'x': (None, 0.15), 'y': (None, None)},
}

ld_cl_bounds = {
    'nt': (),
    'ng': (),
}

clb_cyb_cnb_bounds = {
    'nt': {'clb': (-0.3, 0.02), 'cyb': (-0.5, -0.2), 'cnb': (-0.01, 0.04)},
    'ng': {'clb': (-0.1, 0.01), 'cyb': (-0.4, -0.2), 'cnb': (0.03, 0.07)},
}

cl_cm_cn_bounds = {
    'nt': {'cl': (0.0, 0.006), 'cm': (-0.15, 0.0), 'cn': (-0.002, 0.0)},
    'ng': {'cl': (-0.0015, 0.0015), 'cm': (-0.025, 0.02), 'cn': (-0.001, 0.001)},
}

# CRM 1: NT
ref_area = 0.148     # sqm
ref_span = 0.86      # m
ref_chord = 0.159    # mac [m]

# CRM 2: NG
ref_area = 0.11285535093057521   # sqm
ref_span = 0.66                  # m
ref_chord = 0.19369874002420084  # mac [m]


base_path = Path(__file__).parent / 'data/wind_tunnel/'
save_path = Path('~/Downloads/').expanduser()


def main_wind_tunnel_multi_airspeed_at_sideslip(crm_model, velocities, sideslip, show_fig, save_fig):
    # ------------- C_L vs. C_D ----------------------------------------------------------------------------------------
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=figsize, sharex=True)
    plt.xlabel(r'Drag Coefficient $C_{D}$ [--]')
    plt.ylabel(r'Lift Coefficient $C_{L}$ [--]')

    for idx, velocity in enumerate(velocities):
        # Load in WT results -----------------------------------------------------------------------------------------------
        wt_aero, hdr_wt_aero = load_numpy_with_header(base_path / f'./{crm_model.upper()}/{crm_model.lower()}_wt_aero_{velocity:.1f}ms_beta_{sideslip:.1f}.txt')

        # WT
        ax.plot(wt_aero[:, hdr_wt_aero.index('CD')], wt_aero[:, hdr_wt_aero.index('CL')], marker=MARKERS[idx], color=COLOURS[0], linestyle=LINE_STYLES[idx], linewidth=2, label=rf'{velocity:.1f}$\,$m/s')
        ax.errorbar(x=wt_aero[:, hdr_wt_aero.index('CD')], y=wt_aero[:, hdr_wt_aero.index('CL')], xerr=wt_aero[:, hdr_wt_aero.index('CD_err')], yerr=wt_aero[:, hdr_wt_aero.index('CL_err')], color=COLOURS[0], ecolor=COLOURS[0], capsize=3, fmt='none')

    ax.grid(visible=True, which='major', axis='both', color='black', linestyle='-', linewidth=0.25)  # 0.15
    ax.grid(visible=True, which='minor', axis='both', color='grey', linestyle='--', linewidth=0.15)  # 0.1
    ax.set_xlim(cl_cd_bounds[crm_model.lower()]['x'])
    ax.set_ylim(cl_cd_bounds[crm_model.lower()]['y'])
    ax.legend(loc='best', frameon=False)

    plt.tight_layout()
    # if show_fig:
    #     plt.show()
    if save_fig:
        fig.savefig(Path(save_path) / f"CL_CD_{crm_model.lower()}_wt_beta_{beta:.1f}.png", dpi=200)
    # ------------- C_L vs. C_D ----------------------------------------------------------------------------------------

    # ------------- L/D vs. C_L ----------------------------------------------------------------------------------------
    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=figsize, sharex=True)
    plt.xlabel(r'Lift Coefficient $C_{L}$ [--]')
    plt.ylabel(r'Lift-to-Drag $L/D$ [--]')

    for idx, velocity in enumerate(velocities):
        # Load in WT results -----------------------------------------------------------------------------------------------
        wt_aero, hdr_wt_aero = load_numpy_with_header(base_path / f'./{crm_model.upper()}/{crm_model.lower()}_wt_aero_{velocity:.1f}ms_beta_{sideslip:.1f}.txt')

        # WT
        ax.plot(wt_aero[:, hdr_wt_aero.index('CL')], wt_aero[:, hdr_wt_aero.index('LD')], marker=MARKERS[idx], color=COLOURS[0], linestyle=LINE_STYLES[idx], linewidth=2, label=rf'{velocity:.1f}$\,$m/s')
        ax.errorbar(x=wt_aero[:, hdr_wt_aero.index('CL')], y=wt_aero[:, hdr_wt_aero.index('LD')], xerr=wt_aero[:, hdr_wt_aero.index('CL_err')], yerr=np.abs(wt_aero[:, hdr_wt_aero.index('LD_err')]), color=COLOURS[0], ecolor=COLOURS[0], capsize=3, fmt='none')

    ax.grid(visible=True, which='major', axis='both', color='black', linestyle='-', linewidth=0.25)  # 0.15
    ax.grid(visible=True, which='minor', axis='both', color='grey', linestyle='--', linewidth=0.15)  # 0.1

    ax.legend(loc='best', frameon=False)

    # if xlims is not None:
    #     ax.set_xlim(xlims)
    # ax.set_xlim((None, 1.1))

    plt.tight_layout()
    # if show_fig:
    #     plt.show()
    if save_fig:
        fig.savefig(Path(save_path) / f"LD_CL_{crm_model.lower()}_wt_beta_{beta:.1f}.png", dpi=200)
    # ------------- L/D vs. C_L ----------------------------------------------------------------------------------------

    # ------------- C_l/C_m/C_n vs. alpha ----------------------------------------------------------------------------------------
    # Create figure
    fig, axes = plt.subplots(3, 1, figsize=(9, 9), sharex=True)
    plt.xlabel('Angle of Attack [deg]')

    for idx, velocity in enumerate(velocities):
        # Load in WT results -----------------------------------------------------------------------------------------------
        wt_aero, hdr_wt_aero = load_numpy_with_header(base_path / f'./{crm_model.upper()}/{crm_model.lower()}_wt_aero_{velocity:.1f}ms_beta_{sideslip:.1f}.txt')

        # ----------------------------------------------------------
        ax = fig.axes[0]
        # WT: Cl vs. alpha
        ax.plot(wt_aero[:, hdr_wt_aero.index('alpha')], -wt_aero[:, hdr_wt_aero.index('Cl')], marker=MARKERS[idx], color=COLOURS[0], linestyle=LINE_STYLES[idx], linewidth=2, label=rf'{velocity:.1f}$\,$m/s')
        ax.errorbar(x=wt_aero[:, hdr_wt_aero.index('alpha')], y=-wt_aero[:, hdr_wt_aero.index('Cl')], yerr=np.abs(wt_aero[:, hdr_wt_aero.index('Cl_err')]), color=COLOURS[0], ecolor=COLOURS[0], capsize=3, fmt='none')

        ax.set_xlim(alpha_bounds[crm_model.lower()])
        ax.set_ylim(cl_cm_cn_bounds[crm_model.lower()]['cl'])
        ax.set_ylabel(r'$C_{l}$')
        ax.grid(visible=True, which='major', axis='both', color='black', linestyle='-', linewidth=0.25)  # 0.15
        ax.grid(visible=True, which='minor', axis='both', color='grey', linestyle='--', linewidth=0.15)  # 0.1
        # ax.legend(loc='best', frameon=False)

        # ----------------------------------------------------------
        ax = fig.axes[1]
        # WT: Cm vs. alpha
        ax.plot(wt_aero[:, hdr_wt_aero.index('alpha')], wt_aero[:, hdr_wt_aero.index('Cm')], marker=MARKERS[idx], color=COLOURS[0], linestyle=LINE_STYLES[idx], linewidth=2, label=rf'{velocity:.1f}$\,$m/s')
        ax.errorbar(x=wt_aero[:, hdr_wt_aero.index('alpha')], y=wt_aero[:, hdr_wt_aero.index('Cm')], yerr=np.abs(wt_aero[:, hdr_wt_aero.index('Cm_err')]), color=COLOURS[0], ecolor=COLOURS[0], capsize=3, fmt='none')

        ax.set_xlim(alpha_bounds[crm_model.lower()])
        ax.set_ylim(cl_cm_cn_bounds[crm_model.lower()]['cm'])
        ax.set_ylabel(r'$C_{m}$')
        ax.grid(visible=True, which='major', axis='both', color='black', linestyle='-', linewidth=0.25)  # 0.15
        ax.grid(visible=True, which='minor', axis='both', color='grey', linestyle='--', linewidth=0.15)  # 0.1
        ax.legend(loc='lower left', frameon=False)

        # ----------------------------------------------------------
        ax = fig.axes[2]
        # WT: Cn vs. alpha
        ax.plot(wt_aero[:, hdr_wt_aero.index('alpha')], -wt_aero[:, hdr_wt_aero.index('Cn')], marker=MARKERS[idx], color=COLOURS[0], linestyle=LINE_STYLES[idx], linewidth=2, label=rf'{velocity:.1f}$\,$m/s')
        ax.errorbar(x=wt_aero[:, hdr_wt_aero.index('alpha')], y=-wt_aero[:, hdr_wt_aero.index('Cn')], yerr=np.abs(wt_aero[:, hdr_wt_aero.index('Cn_err')]), color=COLOURS[0], ecolor=COLOURS[0], capsize=3, fmt='none')

        ax.set_xlim(alpha_bounds[crm_model.lower()])
        ax.set_ylim(cl_cm_cn_bounds[crm_model.lower()]['cn'])
        ax.set_ylabel(r'$C_{n}$')
        ax.grid(visible=True, which='major', axis='both', color='black', linestyle='-', linewidth=0.25)  # 0.15
        ax.grid(visible=True, which='minor', axis='both', color='grey', linestyle='--', linewidth=0.15)  # 0.1

    # if xlims is not None:
    #     ax.set_xlim(xlims)

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.1)
    # if show_fig:
    #     plt.show()
    if save_fig:
        fig.savefig(Path(save_path) / f"Cl_Cm_Cn_alpha_{crm_model.lower()}_wt_beta_{beta:.1f}.png", dpi=200)
    # ------------- C_l/C_m/C_n vs. alpha ----------------------------------------------------------------------------------------

    # ------------- Cl_beta/CY_beta/Cn_beta vs. alpha ----------------------------------------------------------------------------------------
    # Create figure
    fig, axes = plt.subplots(3, 1, figsize=(9, 9), sharex=True)
    plt.xlabel('Angle of Attack [deg]')

    for idx, velocity in enumerate(velocities):
        # Load in WT results -----------------------------------------------------------------------------------------------
        wt_aero, hdr_wt_aero = load_numpy_with_header(base_path / f'./{crm_model.upper()}/{crm_model.lower()}_wt_aero_{velocity:.1f}ms_beta_{sideslip:.1f}.txt')
        wt_deriv, hdr_wt_deriv = load_numpy_with_header(base_path / f'./{crm_model.upper()}/{crm_model.lower()}_wt_derivatives_{velocity:.1f}ms_beta_{sideslip:.1f}.txt')

        wt_clmax = np.max(wt_aero[:, hdr_wt_aero.index('CL')])
        wt_ld_max = np.max(wt_aero[:, hdr_wt_aero.index('LD')])
        wt_cd_min = np.min(wt_aero[:, hdr_wt_aero.index('CD')])
        wt_cl_alpha = wt_deriv[:, hdr_wt_deriv.index('CL_alpha')]
        wt_cm_alpha = wt_deriv[:, hdr_wt_deriv.index('Cm_alpha')]
        wt_sm = wt_deriv[:, hdr_wt_deriv.index('SM')]

        is_alpha_0 = np.argmin(np.abs(wt_deriv[:, hdr_wt_deriv.index('alpha')] - 0.))
        wt_cl_beta = -wt_deriv[is_alpha_0, hdr_wt_deriv.index('Cl_beta')]
        wt_cy_beta = -wt_deriv[is_alpha_0, hdr_wt_deriv.index('CY_beta')]
        wt_cn_beta = -wt_deriv[is_alpha_0, hdr_wt_deriv.index('Cn_beta')]
        wt_cl_alpha = wt_cl_alpha[is_alpha_0]
        wt_cm_alpha = wt_cm_alpha[is_alpha_0]
        wt_sm = wt_sm[is_alpha_0]
        
        # Standard Deviations
        clmax_err = wt_aero[np.argmax(wt_aero[:, hdr_wt_aero.index('CL')]), hdr_wt_aero.index('CL_err')]
        ld_max_err = wt_aero[np.argmax(wt_aero[:, hdr_wt_aero.index('LD')]), hdr_wt_aero.index('LD_err')]
        cdmin_err = wt_aero[np.argmin(wt_aero[:, hdr_wt_aero.index('CD')]), hdr_wt_aero.index('CD_err')]
        cl_beta_err = wt_deriv[is_alpha_0, hdr_wt_deriv.index('Cl_beta_err')]
        cy_beta_err = wt_deriv[is_alpha_0, hdr_wt_deriv.index('CY_beta_err')]
        cn_beta_err = wt_deriv[is_alpha_0, hdr_wt_deriv.index('Cn_beta_err')]
        Cla_err = wt_deriv[is_alpha_0, hdr_wt_deriv.index('CL_alpha_err')]
        Cma_err = wt_deriv[is_alpha_0, hdr_wt_deriv.index('Cm_alpha_err')]
        SM_err = wt_deriv[is_alpha_0, hdr_wt_deriv.index('SM_err')]

        print(f'Airspeed: {velocity:.2f}m/s ----------------------------')
        print(f'CL_max\t\tWT: {wt_clmax:.2f}')
        print(f'LD    \t\tWT: {wt_ld_max:.2f}')
        print(f'CD_min\t\tWT: {wt_cd_min:.4f}')
        print(f'CL_a  \t\tWT: {wt_cl_alpha:.2f}')
        print(f'Cm_a  \t\tWT: {wt_cm_alpha:.3f}')
        print(f'SM    \t\tWT: {100 * wt_sm:.2f}')
        print(f'Cl_b  \t\tWT: {wt_cl_beta:.3f}')
        print(f'CY_b  \t\tWT: {wt_cy_beta:.3f}')
        print(f'Cn_b  \t\tWT: {wt_cn_beta:.3f}')
        print(f'Standard Devs ----------------------------')
        print(f'CL_max  err\t\tWT: {clmax_err:.3f}')
        print(f'LD      err\t\tWT: {ld_max_err:.3f}')
        print(f'CD_min  err\t\tWT: {cdmin_err:.4f}')
        print(f'CL_a    err\t\tWT: {Cla_err:.2f}')
        print(f'Cm_a    err\t\tWT: {Cma_err:.3f}')
        print(f'SM      err\t\tWT: {100 * SM_err:.1f}') 
        print(f'Cl_b    err\t\tWT: {cl_beta_err:.3f}')
        print(f'CY_b    err\t\tWT: {cy_beta_err:.3f}')
        print(f'Cn_b    err\t\tWT: {cn_beta_err:.3f}')

        # ----------------------------------------------------------
        ax = fig.axes[0]
        # WT: Cl_beta vs. alpha
        ax.plot(wt_deriv[:, hdr_wt_deriv.index('alpha')], -wt_deriv[:, hdr_wt_deriv.index('Cl_beta')], marker=MARKERS[idx], color=COLOURS[0], linestyle=LINE_STYLES[idx], linewidth=2, label=rf'{velocity:.1f}$\,$m/s')
        ax.errorbar(x=wt_deriv[:, hdr_wt_deriv.index('alpha')], y=-wt_deriv[:, hdr_wt_deriv.index('Cl_beta')], yerr=np.abs(wt_deriv[:, hdr_wt_deriv.index('Cl_beta')]), color=COLOURS[0], ecolor=COLOURS[0], capsize=3, fmt='none')

        ax.set_xlim(alpha_bounds[crm_model.lower()])
        ax.set_ylim(clb_cyb_cnb_bounds[crm_model.lower()]['clb'])
        ax.set_ylabel(r'$C_{l_{\beta}}$')
        ax.grid(visible=True, which='major', axis='both', color='black', linestyle='-', linewidth=0.25)  # 0.15
        ax.grid(visible=True, which='minor', axis='both', color='grey', linestyle='--', linewidth=0.15)  # 0.1
        ax.legend(loc='best', frameon=False)

        # ----------------------------------------------------------
        ax = fig.axes[1]
        # WT: CY_beta vs. alpha
        ax.plot(wt_deriv[:, hdr_wt_deriv.index('alpha')], -wt_deriv[:, hdr_wt_deriv.index('CY_beta')], marker=MARKERS[idx], color=COLOURS[0], linestyle=LINE_STYLES[idx], linewidth=2, label=rf'{velocity:.1f}$\,$m/s')
        ax.errorbar(x=wt_deriv[:, hdr_wt_deriv.index('alpha')], y=-wt_deriv[:, hdr_wt_deriv.index('CY_beta')], yerr=np.abs(wt_deriv[:, hdr_wt_deriv.index('CY_beta_err')]), color=COLOURS[0], ecolor=COLOURS[0], capsize=3, fmt='none')

        ax.set_xlim(alpha_bounds[crm_model.lower()])
        ax.set_ylim(clb_cyb_cnb_bounds[crm_model.lower()]['cyb'])
        ax.set_ylabel(r'$C_{Y_{\beta}}$')
        ax.grid(visible=True, which='major', axis='both', color='black', linestyle='-', linewidth=0.25)  # 0.15
        ax.grid(visible=True, which='minor', axis='both', color='grey', linestyle='--', linewidth=0.15)  # 0.1

        # ----------------------------------------------------------
        ax = fig.axes[2]
        # WT: Cn_beta vs. alpha
        ax.plot(wt_deriv[:, hdr_wt_deriv.index('alpha')], -wt_deriv[:, hdr_wt_deriv.index('Cn_beta')], marker=MARKERS[idx], color=COLOURS[0], linestyle=LINE_STYLES[idx], linewidth=2, label=rf'{velocity:.1f}$\,$m/s')
        ax.errorbar(x=wt_deriv[:, hdr_wt_deriv.index('alpha')], y=-wt_deriv[:, hdr_wt_deriv.index('Cn_beta')], yerr=np.abs(wt_deriv[:, hdr_wt_deriv.index('Cn_beta_err')]), color=COLOURS[0], ecolor=COLOURS[0], capsize=3, fmt='none')

        ax.set_xlim(alpha_bounds[crm_model.lower()])
        ax.set_ylim(clb_cyb_cnb_bounds[crm_model.lower()]['cnb'])
        ax.set_ylabel(r'$C_{n_{\beta}}$')
        ax.grid(visible=True, which='major', axis='both', color='black', linestyle='-', linewidth=0.25)  # 0.15
        ax.grid(visible=True, which='minor', axis='both', color='grey', linestyle='--', linewidth=0.15)  # 0.1

    plt.tight_layout()
    if show_fig:
        plt.show()
    if save_fig:
        fig.savefig(Path(save_path) / f"Cl_b_CY_b_Cn_b_alpha_{crm_model.lower()}_wt_beta_{beta:.1f}.png", dpi=200)
    # ------------- Cl_beta/CY_beta/Cn_beta vs. alpha ----------------------------------------------------------------------------------------


if __name__ == '__main__':
    # Parameters to change
    crm_model = 'NG'  # 'NT' or 'NG'
    airspeeds = [15., 17.5, 20., 22.5, 25.]
    # airspeeds = [15., 20., 25.]
    beta = 0.0   # -2.5, 0.0, 2.5

    main_wind_tunnel_multi_airspeed_at_sideslip(crm_model=crm_model, velocities=airspeeds, sideslip=beta, show_fig=False, save_fig=False)
