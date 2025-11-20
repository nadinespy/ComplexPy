#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Plotting functions for emergence measure heatmaps.

Creates heatmaps with noise_corr on x-axis and coupling on y-axis.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


def plot_emergence_heatmap(emergence_df, measure, title=None, ax=None, cmap="coolwarm",
                           figsize=(8, 6), **filter_params):
    """
    Plot a single heatmap for an emergence measure.

    Parameters
    ----------
    emergence_df : pd.DataFrame
        DataFrame from compute_emergence()
    measure : str
        Measure to plot (e.g., 'phiid_wpe', 'shannon_dc')
    title : str, optional
        Plot title. If None, uses measure name.
    ax : matplotlib.axes.Axes, optional
        Axes to plot on. If None, creates new figure.
    cmap : str, optional
        Colormap name. Default is 'coolwarm'.
    figsize : tuple, optional
        Figure size if creating new figure.
    **filter_params : dict
        Additional filters (e.g., time_lag_for_measure=1, red_func='mmi')

    Returns
    -------
    ax : matplotlib.axes.Axes
        The axes with the heatmap.
    """
    # Filter data for the specific measure
    df_filtered = emergence_df[emergence_df['measure'] == measure].copy()

    # Apply additional filters
    for param, value in filter_params.items():
        if param in df_filtered.columns:
            df_filtered = df_filtered[df_filtered[param] == value]

    if df_filtered.empty:
        raise ValueError(f"No data found for measure '{measure}' with filters {filter_params}")

    # Create pivot table: coupling (y-axis) vs noise_corr (x-axis)
    pivot_table = pd.pivot_table(
        df_filtered,
        values='value',
        index='coupling',
        columns='noise_corr',
        aggfunc='mean'
    )

    # Sort index for proper display (low to high coupling on y-axis)
    pivot_table = pivot_table.sort_index(ascending=False)

    # Create figure if needed
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    # Create heatmap
    sns.heatmap(
        pivot_table,
        cmap=cmap,
        ax=ax,
        cbar_kws={'label': 'Value'}
    )

    # Format tick labels
    n_xticks = min(10, len(pivot_table.columns))
    n_yticks = min(10, len(pivot_table.index))

    xtick_positions = np.linspace(0, len(pivot_table.columns) - 1, n_xticks, dtype=int)
    ytick_positions = np.linspace(0, len(pivot_table.index) - 1, n_yticks, dtype=int)

    ax.set_xticks(xtick_positions + 0.5)
    ax.set_xticklabels([f"{pivot_table.columns[i]:.2f}" for i in xtick_positions], rotation=45)
    ax.set_yticks(ytick_positions + 0.5)
    ax.set_yticklabels([f"{pivot_table.index[i]:.2f}" for i in ytick_positions])

    # Labels
    ax.set_xlabel('Noise Correlation')
    ax.set_ylabel('Coupling')

    # Title
    if title is None:
        title = measure
        if filter_params:
            filter_str = ', '.join([f"{k}={v}" for k, v in filter_params.items()])
            title = f"{measure} ({filter_str})"
    ax.set_title(title)

    return ax


def plot_all_measures(emergence_df, measures=None, ncols=3, figsize_per_plot=(5, 4),
                      cmap="coolwarm", save_path=None, **filter_params):
    """
    Plot heatmaps for multiple measures in a grid.

    Parameters
    ----------
    emergence_df : pd.DataFrame
        DataFrame from compute_emergence()
    measures : list, optional
        List of measures to plot. If None, plots all unique measures.
    ncols : int, optional
        Number of columns in grid.
    figsize_per_plot : tuple, optional
        Size of each subplot.
    cmap : str, optional
        Colormap name.
    save_path : str, optional
        Path to save figure. If None, doesn't save.
    **filter_params : dict
        Filters applied to all plots.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The figure with all heatmaps.
    """
    if measures is None:
        measures = emergence_df['measure'].unique().tolist()

    nrows = int(np.ceil(len(measures) / ncols))
    figsize = (figsize_per_plot[0] * ncols, figsize_per_plot[1] * nrows)

    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    axes = np.atleast_2d(axes)

    for idx, measure in enumerate(measures):
        row = idx // ncols
        col = idx % ncols
        ax = axes[row, col]

        try:
            plot_emergence_heatmap(
                emergence_df,
                measure,
                ax=ax,
                cmap=cmap,
                **filter_params
            )
        except ValueError as e:
            ax.text(0.5, 0.5, str(e), ha='center', va='center', transform=ax.transAxes)
            ax.set_title(measure)

    # Hide empty subplots
    for idx in range(len(measures), nrows * ncols):
        row = idx // ncols
        col = idx % ncols
        axes[row, col].set_visible(False)

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved figure to {save_path}")

    return fig


def plot_parameter_comparison(emergence_df, measure, compare_param, compare_values,
                              ncols=None, figsize_per_plot=(5, 4), cmap="coolwarm",
                              save_path=None, **filter_params):
    """
    Plot heatmaps comparing different values of a parameter.

    Parameters
    ----------
    emergence_df : pd.DataFrame
        DataFrame from compute_emergence()
    measure : str
        Measure to plot.
    compare_param : str
        Parameter to compare (e.g., 'time_lag_for_measure', 'red_func')
    compare_values : list
        Values to compare.
    ncols : int, optional
        Number of columns. If None, uses len(compare_values).
    figsize_per_plot : tuple, optional
        Size of each subplot.
    cmap : str, optional
        Colormap name.
    save_path : str, optional
        Path to save figure.
    **filter_params : dict
        Additional filters applied to all plots.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The figure with comparison heatmaps.
    """
    if ncols is None:
        ncols = len(compare_values)

    nrows = int(np.ceil(len(compare_values) / ncols))
    figsize = (figsize_per_plot[0] * ncols, figsize_per_plot[1] * nrows)

    fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
    if len(compare_values) == 1:
        axes = np.array([[axes]])
    else:
        axes = np.atleast_2d(axes)

    for idx, value in enumerate(compare_values):
        row = idx // ncols
        col = idx % ncols
        ax = axes[row, col]

        # Add the comparison parameter to filters
        current_filters = {**filter_params, compare_param: value}

        try:
            plot_emergence_heatmap(
                emergence_df,
                measure,
                title=f"{measure}\n{compare_param}={value}",
                ax=ax,
                cmap=cmap,
                **current_filters
            )
        except ValueError as e:
            ax.text(0.5, 0.5, str(e), ha='center', va='center',
                   transform=ax.transAxes, wrap=True)
            ax.set_title(f"{measure}\n{compare_param}={value}")

    # Hide empty subplots
    for idx in range(len(compare_values), nrows * ncols):
        row = idx // ncols
        col = idx % ncols
        axes[row, col].set_visible(False)

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved figure to {save_path}")

    return fig


# Example usage
if __name__ == "__main__":
    # Define paths
    pathout_analyses = 'results/analyses/'
    pathout_plots = 'results/plots/'

    # Load emergence_df from pickle
    filepath = f'{pathout_analyses}emergence_results.pkl'

    import os
    if os.path.exists(filepath):
        emergence_df = pd.read_pickle(filepath)
        print(f"Loaded emergence_df from {filepath}")
        print(f"Shape: {emergence_df.shape}")

        # Get unique values for all parameters
        measures = emergence_df['measure'].unique().tolist()
        time_lags_model = sorted(emergence_df['time_lag_for_model'].unique().tolist()) if 'time_lag_for_model' in emergence_df.columns else [None]
        time_lags_measure = sorted(emergence_df['time_lag_for_measure'].unique().tolist()) if 'time_lag_for_measure' in emergence_df.columns else [None]
        red_funcs = emergence_df['red_func'].unique().tolist() if 'red_func' in emergence_df.columns else [None]

        print(f"Measures: {measures}")
        print(f"Time lags (model): {time_lags_model}")
        print(f"Time lags (measure): {time_lags_measure}")
        print(f"Redundancy functions: {red_funcs}")

        # Create output directory
        os.makedirs(pathout_plots, exist_ok=True)

        # Generate one plot per measure for each parameter combination
        print("\n--- Generating individual heatmaps ---")

        plot_count = 0
        for measure in measures:
            for time_lag_model in time_lags_model:
                for time_lag_measure in time_lags_measure:
                    for red_func in red_funcs:
                        # Filter data for this specific combination
                        df_filtered = emergence_df[emergence_df['measure'] == measure].copy()

                        if time_lag_model is not None:
                            df_filtered = df_filtered[df_filtered['time_lag_for_model'] == time_lag_model]
                        if time_lag_measure is not None:
                            df_filtered = df_filtered[df_filtered['time_lag_for_measure'] == time_lag_measure]
                        if red_func is not None:
                            df_filtered = df_filtered[df_filtered['red_func'] == red_func]

                        if df_filtered.empty:
                            continue

                        # Build filename
                        filename_parts = [measure]
                        if time_lag_model is not None:
                            filename_parts.append(f'modellag{time_lag_model}')
                        if time_lag_measure is not None:
                            filename_parts.append(f'measurelag{time_lag_measure}')
                        if red_func is not None:
                            filename_parts.append(red_func)

                        filename = '_'.join(filename_parts) + '.png'
                        save_path = f'{pathout_plots}{filename}'

                        # Create pivot table for this specific combination
                        pivot_table = pd.pivot_table(
                            df_filtered,
                            values='value',
                            index='coupling',
                            columns='noise_corr',
                            aggfunc='first'  # Should only be one value per cell
                        )
                        pivot_table = pivot_table.sort_index(ascending=False)

                        # Create single plot
                        fig, ax = plt.subplots(figsize=(8, 6))

                        sns.heatmap(
                            pivot_table,
                            cmap="coolwarm",
                            ax=ax,
                            cbar_kws={'label': 'Value'}
                        )

                        # Format tick labels
                        n_xticks = min(10, len(pivot_table.columns))
                        n_yticks = min(10, len(pivot_table.index))

                        xtick_positions = np.linspace(0, len(pivot_table.columns) - 1, n_xticks, dtype=int)
                        ytick_positions = np.linspace(0, len(pivot_table.index) - 1, n_yticks, dtype=int)

                        ax.set_xticks(xtick_positions + 0.5)
                        ax.set_xticklabels([f"{pivot_table.columns[i]:.2f}" for i in xtick_positions], rotation=45)
                        ax.set_yticks(ytick_positions + 0.5)
                        ax.set_yticklabels([f"{pivot_table.index[i]:.2f}" for i in ytick_positions])

                        ax.set_xlabel('Noise Correlation')
                        ax.set_ylabel('Coupling')

                        # Build title
                        title_parts = [measure]
                        if time_lag_model is not None:
                            title_parts.append(f'model_lag={time_lag_model}')
                        if time_lag_measure is not None:
                            title_parts.append(f'measure_lag={time_lag_measure}')
                        if red_func is not None:
                            title_parts.append(f'red_func={red_func}')
                        ax.set_title(', '.join(title_parts))

                        plt.tight_layout()
                        fig.savefig(save_path, dpi=300, bbox_inches='tight')
                        plt.close(fig)
                        print(f"Saved: {filename}")
                        plot_count += 1

        print(f"\n--- Done! Generated {plot_count} plots in {pathout_plots} ---")

    else:
        print(f"File not found: {filepath}")
        print("Run compute_emergence() first and save the results.")
        print("\nUsage:")
        print("  - plot_emergence_heatmap(emergence_df, 'phiid_wpe')")
        print("  - plot_all_measures(emergence_df)")
        print("  - plot_parameter_comparison(emergence_df, 'phiid_wpe', 'time_lag_for_model', [1, 10])")