"""
Script to parse a music game XML map file and plot the real-time Keys-Per-Second (KPS) curve.

Usage:
    python kps_plot.py path/to/map.xml [--window 1.0] [--step 0.1] [--output kps.png] [--width 10] [--unicode]

Options:
    --window   Size of the sliding window in seconds (default: 1.0)
    --step     Step size in seconds for sampling (default: 0.1)
    --output   Path to save the output plot image (if omitted, displays interactively)
    --width    Width of the plot figure (default: 10)
    --unicode  Use SimHei font for Unicode character support (e.g., Chinese)
"""
import argparse
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os

def parse_times_and_title(xml_file: str):
    """
    Parse the XML file and extract all note times (in seconds) and title.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    times = []
    for note in root.findall('.//CMapNoteAsset'):
        t_elem = note.find('m_time')
        if t_elem is not None:
            try:
                times.append(float(t_elem.text))
            except (TypeError, ValueError):
                continue
    # Extract <m_path>, <m_mapID> for title
    m_path = root.find('.//m_path')
    m_mapID = root.find('.//m_mapID')
    title = (m_path.text if m_path is not None and m_path.text else
             m_mapID.text if m_mapID is not None and m_mapID.text else
             os.path.basename(xml_file))
    return sorted(times), title

def compute_kps(times: list, window: float = 1.0, step: float = 0.1):
    """
    Compute KPS (keys per second) using a sliding window.

    Returns:
        t   : numpy array of time stamps (start of each window)
        kps : numpy array of KPS values
    """
    if not times:
        return np.array([]), np.array([])
    max_time = times[-1]
    t = np.arange(0, max_time + step, step)
    counts = np.zeros_like(t)
    idx = 0
    n = len(times)
    for i, start in enumerate(t):
        while idx < n and times[idx] < start:
            idx += 1
        j = idx
        while j < n and times[j] < start + window:
            j += 1
        counts[i] = j - idx
    kps = counts / window
    return t, kps

def plot_kps(t: np.ndarray, kps: np.ndarray, title: str = None, output: str = None, width: float = 10):
    """
    Plot the KPS curve.
    """
    plt.figure(figsize=(width, 5))
    plt.plot(t, kps, linewidth=2)
    plt.xlabel('Time (s)')
    plt.ylabel('Keys per Second (KPS)')
    if title:
        plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    if output:
        plt.savefig(output)
        print(f"Saved KPS plot to {output}")
    else:
        plt.show()

def main():
    parser = argparse.ArgumentParser(
        description='Plot real-time KPS from a music game XML map file.'
    )
    parser.add_argument('xml_file', help='Path to the XML map file')
    parser.add_argument('--window', type=float, default=1.0,
                        help='Sliding window size in seconds')
    parser.add_argument('--step', type=float, default=0.1,
                        help='Time step in seconds')
    parser.add_argument('--output', help='Output image file path')
    parser.add_argument('--width', type=float, default=10,
                        help='Width of the plot figure')
    parser.add_argument('--unicode', action='store_true',
                        help='Use SimHei font for Unicode characters')
    args = parser.parse_args()

    if args.unicode:
        matplotlib.rcParams['font.family'] = 'SimHei'
    else:
        matplotlib.rcParams['font.family'] = 'DejaVu Sans'
    matplotlib.rcParams['axes.unicode_minus'] = False

    times, title = parse_times_and_title(args.xml_file)
    if not times:
        print("No note times found in the XML file.")
        return

    t, kps = compute_kps(times, args.window, args.step)
    plot_kps(t, kps, title=title, output=args.output, width=args.width)

if __name__ == '__main__':
    main()