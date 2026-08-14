#!/usr/bin/env python3
"""Generate editable Excalidraw scenes and matching SVG exports.

The script intentionally uses only the Python standard library. Diagram
definitions live beside the renderer so the JSON and SVG stay synchronized.
"""

from __future__ import annotations

import hashlib
import html
import json
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_ROOT / "book" / "excalidraw"

INK = "#1e1e1e"
MUTED = "#495057"
WHITE = "#ffffff"
BLUE = ("#1971c2", "#a5d8ff")
GREEN = ("#2f9e44", "#b2f2bb")
ORANGE = ("#e8590c", "#ffd8a8")
YELLOW = ("#e67700", "#ffec99")
RED = ("#c92a2a", "#ffc9c9")
VIOLET = ("#6741d9", "#d0bfff")
CYAN = ("#0b7285", "#c5f6fa")
GREY = ("#495057", "#e9ecef")


def stable_int(value: str) -> int:
    """Return a deterministic positive 31-bit integer."""
    return int(hashlib.sha256(value.encode()).hexdigest()[:8], 16) & 0x7FFFFFFF


@dataclass
class Scene:
    """Small common drawing surface for Excalidraw JSON and SVG."""

    slug: str
    title: str
    description: str
    width: int
    height: int
    source_assets: list[str] = field(default_factory=list)
    elements: list[dict[str, Any]] = field(default_factory=list)
    svg_parts: list[str] = field(default_factory=list)

    def _base(self, element_type: str, x: float, y: float, width: float, height: float) -> dict[str, Any]:
        order = len(self.elements)
        identity = f"{self.slug}:{order}:{element_type}"
        return {
            "id": hashlib.sha256(identity.encode()).hexdigest()[:12],
            "type": element_type,
            "x": round(x, 2),
            "y": round(y, 2),
            "width": round(width, 2),
            "height": round(height, 2),
            "angle": 0,
            "strokeColor": INK,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 2,
            "strokeStyle": "solid",
            "roughness": 0,
            "opacity": 100,
            "groupIds": [],
            "frameId": None,
            "index": f"a{order:03x}",
            "roundness": None,
            "seed": stable_int(identity),
            "version": 1,
            "versionNonce": stable_int(identity + ":nonce"),
            "isDeleted": False,
            "boundElements": [],
            "updated": 1,
            "link": None,
            "locked": False,
            "customData": {"provenance": "AI-generated"},
        }

    def text(
        self,
        cx: float,
        cy: float,
        value: str,
        *,
        size: int = 20,
        color: str = INK,
        align: str = "center",
        weight: int = 400,
    ) -> None:
        lines = value.splitlines() or [""]
        width = max(1, max(len(line) for line in lines)) * size * 0.56
        height = len(lines) * size * 1.25
        x = cx - width / 2 if align == "center" else cx
        y = cy - height / 2
        element = self._base("text", x, y, width, height)
        element.update(
            {
                "strokeColor": color,
                "fontSize": size,
                "fontFamily": 5,
                "text": value,
                "textAlign": align,
                "verticalAlign": "middle",
                "containerId": None,
                "originalText": value,
                "autoResize": True,
                "lineHeight": 1.25,
            }
        )
        self.elements.append(element)

        anchor = "middle" if align == "center" else "start"
        line_height = size * 1.25
        first_y = cy - (len(lines) - 1) * line_height / 2
        tspans = "".join(
            f'<tspan x="{cx}" y="{first_y + i * line_height}">{html.escape(line)}</tspan>'
            for i, line in enumerate(lines)
        )
        self.svg_parts.append(
            f'<text text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}" font-family="Inter, system-ui, sans-serif">{tspans}</text>'
        )

    def heading(self, value: str) -> None:
        self.text(self.width / 2, 35, value, size=28, weight=500)

    def rect(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        *,
        stroke: str = INK,
        fill: str = "transparent",
        dashed: bool = False,
        radius: int = 12,
        stroke_width: int = 2,
    ) -> None:
        element = self._base("rectangle", x, y, width, height)
        element.update(
            {
                "strokeColor": stroke,
                "backgroundColor": fill,
                "strokeWidth": stroke_width,
                "strokeStyle": "dashed" if dashed else "solid",
                "roundness": {"type": 3},
            }
        )
        self.elements.append(element)
        dash = ' stroke-dasharray="9 7"' if dashed else ""
        self.svg_parts.append(
            f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"{dash}/>'
        )

    def box(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        label: str,
        *,
        colors: tuple[str, str] = BLUE,
        size: int = 20,
        dashed: bool = False,
    ) -> None:
        self.rect(x, y, width, height, stroke=colors[0], fill=colors[1], dashed=dashed)
        self.text(x + width / 2, y + height / 2, label, size=size)

    def ellipse(
        self,
        cx: float,
        cy: float,
        rx: float,
        ry: float,
        label: str = "",
        *,
        colors: tuple[str, str] = BLUE,
        size: int = 20,
    ) -> None:
        element = self._base("ellipse", cx - rx, cy - ry, rx * 2, ry * 2)
        element.update({"strokeColor": colors[0], "backgroundColor": colors[1]})
        self.elements.append(element)
        self.svg_parts.append(
            f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" '
            f'fill="{colors[1]}" stroke="{colors[0]}" stroke-width="2"/>'
        )
        if label:
            self.text(cx, cy, label, size=size)

    def arrow(
        self,
        points: list[tuple[float, float]],
        *,
        color: str = MUTED,
        label: str | None = None,
        label_offset: tuple[float, float] = (0, -15),
        dashed: bool = False,
        start_arrow: bool = False,
    ) -> None:
        x, y = points[0]
        relative = [[round(px - x, 2), round(py - y, 2)] for px, py in points]
        xs = [p[0] for p in relative]
        ys = [p[1] for p in relative]
        element = self._base("arrow", x, y, max(xs) - min(xs), max(ys) - min(ys))
        element.update(
            {
                "strokeColor": color,
                "strokeStyle": "dashed" if dashed else "solid",
                "points": relative,
                "lastCommittedPoint": None,
                "startBinding": None,
                "endBinding": None,
                "startArrowhead": "arrow" if start_arrow else None,
                "endArrowhead": "arrow",
                "elbowed": len(points) > 2,
            }
        )
        self.elements.append(element)
        path = " ".join(f"{px},{py}" for px, py in points)
        dash = ' stroke-dasharray="9 7"' if dashed else ""
        start = ' marker-start="url(#arrow-start)"' if start_arrow else ""
        self.svg_parts.append(
            f'<polyline points="{path}" fill="none" stroke="{color}" stroke-width="2" '
            f'stroke-linejoin="round" marker-end="url(#arrow-end)"{start}{dash}/>'
        )
        if label:
            lengths = [
                math.hypot(end[0] - start[0], end[1] - start[1])
                for start, end in zip(points[:-1], points[1:], strict=True)
            ]
            target = sum(lengths) / 2
            traversed = 0.0
            label_x, label_y = points[0]
            for start, end, length in zip(points[:-1], points[1:], lengths, strict=True):
                if traversed + length >= target:
                    ratio = (target - traversed) / length if length else 0
                    label_x = start[0] + (end[0] - start[0]) * ratio
                    label_y = start[1] + (end[1] - start[1]) * ratio
                    break
                traversed += length
            self.text(label_x + label_offset[0], label_y + label_offset[1], label, size=16)

    def line(
        self,
        points: list[tuple[float, float]],
        *,
        color: str = MUTED,
        dashed: bool = False,
        stroke_width: int = 2,
    ) -> None:
        x, y = points[0]
        relative = [[round(px - x, 2), round(py - y, 2)] for px, py in points]
        xs = [p[0] for p in relative]
        ys = [p[1] for p in relative]
        element = self._base("line", x, y, max(xs) - min(xs), max(ys) - min(ys))
        element.update(
            {
                "strokeColor": color,
                "strokeWidth": stroke_width,
                "strokeStyle": "dashed" if dashed else "solid",
                "points": relative,
                "lastCommittedPoint": None,
                "startBinding": None,
                "endBinding": None,
                "startArrowhead": None,
                "endArrowhead": None,
            }
        )
        self.elements.append(element)
        path = " ".join(f"{px},{py}" for px, py in points)
        dash = ' stroke-dasharray="9 7"' if dashed else ""
        self.svg_parts.append(
            f'<polyline points="{path}" fill="none" stroke="{color}" '
            f'stroke-width="{stroke_width}" stroke-linejoin="round"{dash}/>'
        )

    def write(self) -> None:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        archived_sources = [
            asset
            if asset.startswith("archive/original-images/")
            else f"archive/original-images/{asset}"
            for asset in self.source_assets
        ]
        scene = {
            "type": "excalidraw",
            "version": 2,
            "source": "https://excalidraw.com",
            "elements": self.elements,
            "appState": {
                "gridSize": None,
                "viewBackgroundColor": WHITE,
                "currentItemFontFamily": 5,
            },
            "files": {},
            "metadata": {
                "provenance": "AI-generated",
                "description": self.description,
                "sourceAssets": archived_sources,
            },
        }
        (OUTPUT_DIR / f"{self.slug}.json").write_text(
            json.dumps(scene, indent=2) + "\n", encoding="utf-8"
        )

        metadata = html.escape(
            json.dumps(
                {
                    "provenance": "AI-generated",
                    "sourceAssets": archived_sources,
                }
            )
        )
        svg = "\n".join(
            [
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.width} {self.height}" '
                'width="100%" role="img">',
                f"  <title>{html.escape(self.title)}</title>",
                f"  <desc>{html.escape(self.description)}</desc>",
                f"  <metadata>{metadata}</metadata>",
                "  <defs>",
                '    <marker id="arrow-end" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="context-stroke"/></marker>',
                '    <marker id="arrow-start" markerWidth="10" markerHeight="10" refX="1" refY="3" orient="auto-start-reverse" markerUnits="strokeWidth"><path d="M9,0 L9,6 L0,3 z" fill="context-stroke"/></marker>',
                "  </defs>",
                '  <rect width="100%" height="100%" fill="#ffffff"/>',
                *(f"  {part}" for part in self.svg_parts),
                "</svg>",
                "",
            ]
        )
        (OUTPUT_DIR / f"{self.slug}.svg").write_text(svg, encoding="utf-8")


def kubernetes_nodeport_single() -> Scene:
    s = Scene(
        "kubernetes-nodeport-single",
        "NodePort Service on one node",
        "A request to node IP 192.168.1.2 on NodePort 30008 is routed by a Service to one of three Pods.",
        960,
        680,
        ["book/images/nodeport.png"],
    )
    s.heading("NodePort on one node")
    s.ellipse(480, 105, 75, 32, "Client", colors=GREY)
    s.rect(120, 165, 720, 455, stroke=GREY[0], fill="#f8f9fa", dashed=True)
    s.text(185, 195, "Node 192.168.1.2", size=20, align="left", weight=500)
    s.box(380, 220, 200, 58, "NodePort 30008", colors=ORANGE)
    s.box(340, 335, 280, 68, "Service :80", colors=CYAN)
    pods = [(190, "Pod\n10.244.0.3"), (390, "Pod\n10.244.0.2"), (590, "Pod\n10.244.0.4")]
    s.arrow([(480, 137), (480, 220)], label="192.168.1.2:30008", label_offset=(145, -30))
    s.arrow([(480, 278), (480, 335)])
    for x, label in pods:
        s.arrow([(480, 403), (x + 90, 485)])
        s.box(x, 485, 180, 90, label, colors=BLUE, size=18)
    return s


def kubernetes_nodeport_cluster() -> Scene:
    s = Scene(
        "kubernetes-nodeport-cluster",
        "NodePort Service across a cluster",
        "The same NodePort 30008 is reachable on every node and routes through one Service to Pods on any node.",
        1180,
        720,
        ["book/images/nodeport1.png"],
    )
    s.heading("The same NodePort is exposed on every node")
    s.ellipse(590, 102, 75, 32, "Client", colors=GREY)
    node_xs = [80, 425, 770]
    node_ips = ["192.168.1.2", "192.168.1.3", "192.168.1.4"]
    pod_ips = ["10.244.0.3", "10.244.0.2", "10.244.0.4"]
    for x, node_ip, pod_ip in zip(node_xs, node_ips, pod_ips, strict=True):
        s.rect(x, 230, 300, 420, stroke=GREY[0], fill="#f8f9fa", dashed=True)
        s.text(x + 150, 258, f"Node {node_ip}", size=18, weight=500)
        s.box(x + 65, 295, 170, 55, "NodePort 30008", colors=ORANGE, size=17)
        s.box(x + 65, 515, 170, 82, f"Pod\n{pod_ip}", colors=BLUE, size=17)
        s.arrow([(590, 134), (x + 150, 295)], dashed=True)
    s.box(350, 395, 480, 70, "One virtual Service routes across the cluster", colors=CYAN, size=19)
    for x in node_xs:
        s.arrow([(x + 150, 350), (x + 150, 395)], color=ORANGE[0])
        s.arrow([(590, 465), (x + 150, 515)])
    s.text(590, 685, "Client may use :30008 on any node IP; the selected backend Pod may run elsewhere.", size=17)
    return s


def kubernetes_clusterip() -> Scene:
    s = Scene(
        "kubernetes-clusterip",
        "ClusterIP Services connecting three application tiers",
        "Front-end Pods reach back-end Pods through a back-end Service, and back-end Pods reach Redis Pods through a Redis Service.",
        1120,
        780,
        ["book/images/clusterip.png"],
    )
    s.heading("Stable ClusterIP Services connect changing Pods")
    rows = [
        (105, "front-end", ["10.244.0.3", "10.244.0.2", "10.244.0.4"], BLUE),
        (360, "back-end", ["10.244.0.5", "10.244.0.6", "10.244.0.7"], GREEN),
        (615, "redis", ["10.244.0.8", "10.244.0.9", "10.244.0.10"], RED),
    ]
    centers = [335, 575, 815]
    for y, tier, ips, colors in rows:
        s.text(55, y + 50, tier, size=20, align="left", weight=500)
        for cx, ip in zip(centers, ips, strict=True):
            s.box(cx - 90, y, 180, 100, f"Pod\n{ip}", colors=colors, size=17)
    s.box(270, 250, 610, 65, "back-end Service (stable ClusterIP)", colors=CYAN, size=19)
    s.box(270, 505, 610, 65, "redis Service (stable ClusterIP)", colors=ORANGE, size=19)
    for cx in centers:
        s.arrow([(cx, 205), (cx, 250)], color=BLUE[0])
        s.arrow([(560, 315), (cx, 360)], color=CYAN[0])
        s.arrow([(cx, 460), (cx, 505)], color=GREEN[0])
        s.arrow([(560, 570), (cx, 615)], color=ORANGE[0])
    return s


def java_heap_layout() -> Scene:
    s = Scene(
        "java-heap-layout",
        "HotSpot memory layout before and after Java 8",
        "Before Java 8, PermGen was inside the heap; Java 8 replaced it with native-memory Metaspace outside the heap.",
        1100,
        680,
        ["book/java/images/gc1.png"],
    )
    s.heading("PermGen was replaced by native-memory Metaspace")
    for x, era in [(90, "Before Java 8"), (590, "Java 8+")]:
        s.text(x + 210, 105, era, size=24, weight=500)
        s.rect(x, 145, 420, 465, stroke=GREY[0], fill="#f8f9fa")
        s.text(x + 210, 632, "JVM process", size=18, weight=500)
    s.rect(135, 185, 330, 290, stroke=BLUE[0], fill="#e7f5ff", dashed=True)
    s.text(160, 205, "Heap (-Xmx)", size=18, align="left", weight=500)
    s.box(170, 240, 260, 85, "New generation\n(Eden + Survivors)", colors=GREEN, size=17)
    s.box(170, 335, 260, 65, "Old generation", colors=YELLOW, size=18)
    s.box(170, 410, 260, 45, "PermGen (-XX:MaxPermSize)", colors=ORANGE, size=15)
    s.text(300, 545, "Native memory", size=19)

    s.rect(635, 185, 330, 215, stroke=BLUE[0], fill="#e7f5ff", dashed=True)
    s.text(660, 205, "Heap (-Xmx)", size=18, align="left", weight=500)
    s.box(670, 240, 260, 75, "New generation\n(Eden + Survivors)", colors=GREEN, size=17)
    s.box(670, 325, 260, 55, "Old generation", colors=YELLOW, size=18)
    s.box(670, 455, 260, 65, "Metaspace\n(-XX:MaxMetaspaceSize)", colors=ORANGE, size=16)
    s.text(800, 555, "Native memory", size=19)
    s.arrow([(465, 432), (670, 487)], label="replaced", label_offset=(0, -22))
    return s


def java_generational_heap() -> Scene:
    s = Scene(
        "java-generational-heap",
        "Conceptual generational heap",
        "New objects enter Eden, survivors alternate between survivor spaces, and sufficiently long-lived objects are promoted to the old generation.",
        1100,
        450,
        ["book/java/images/gc.png"],
    )
    s.heading("Conceptual generational heap")
    s.text(370, 105, "Young generation", size=23, weight=500)
    s.text(865, 105, "Old generation", size=23, weight=500)
    s.box(180, 150, 380, 110, "Eden", colors=GREEN, size=28)
    s.box(570, 150, 115, 110, "S0", colors=BLUE, size=26)
    s.box(695, 150, 115, 110, "S1", colors=BLUE, size=26)
    s.box(820, 150, 220, 110, "Tenured", colors=YELLOW, size=28)
    s.arrow([(50, 205), (180, 205)], label="new objects", label_offset=(0, -20))
    s.arrow([(560, 285), (570, 330), (752, 330), (752, 260)], label="survivors alternate S0 ↔ S1", label_offset=(0, 22), start_arrow=True)
    s.arrow([(810, 205), (820, 205)], label="promotion", label_offset=(0, -20))
    s.text(550, 405, "This is a teaching model; region-based collectors do not require contiguous generations.", size=17)
    return s


def java_contiguous_vs_g1() -> Scene:
    s = Scene(
        "java-contiguous-vs-g1-regions",
        "Fixed contiguous heap spaces compared with G1 regions",
        "A traditional teaching layout uses contiguous Eden, survivor, and old spaces; G1 assigns equal-sized regions dynamically as unused, survivor, Eden, or old.",
        1180,
        580,
        ["book/java/images/gc3spaces.png", "book/java/images/g1gc.png"],
    )
    s.heading("Contiguous spaces versus G1 regions")
    s.text(90, 105, "Earlier teaching model", size=20, align="left", weight=500)
    s.box(90, 135, 420, 80, "Old", colors=ORANGE, size=22)
    s.box(510, 135, 250, 80, "Survivor", colors=YELLOW, size=22)
    s.box(760, 135, 330, 80, "Eden", colors=GREEN, size=22)
    s.text(90, 285, "G1 equal-sized regions", size=20, align="left", weight=500)
    labels = list("USUSEOUUUEEOSSSUOEO")
    colors = {"U": GREY, "S": GREEN, "E": YELLOW, "O": ORANGE}
    x0, y0, cell_w, cell_h = 90, 325, 50, 72
    for index, label in enumerate(labels):
        s.box(x0 + index * cell_w, y0, cell_w, cell_h, label, colors=colors[label], size=18)
    legend = [("U", "unused", GREY), ("S", "survivor", GREEN), ("E", "Eden", YELLOW), ("O", "old", ORANGE)]
    for index, (key, label, palette) in enumerate(legend):
        x = 140 + index * 250
        s.box(x, 455, 45, 45, key, colors=palette, size=16)
        s.text(x + 60, 478, label, size=17, align="left")
    s.text(590, 545, "Region roles change as G1 selects regions for allocation and evacuation.", size=17)
    return s


def java_thread_states() -> Scene:
    s = Scene(
        "java-thread-states",
        "Java thread lifecycle states",
        "Transitions among NEW, RUNNABLE, BLOCKED, WAITING, TIMED_WAITING, and TERMINATED with representative causes.",
        1220,
        750,
        ["book/java/images/threadlifecycle.png"],
    )
    s.heading("Java exposes six Thread.State values")
    s.box(50, 145, 200, 80, "NEW", colors=GREEN, size=22)
    s.box(430, 135, 320, 95, "RUNNABLE\n(eligible or running)", colors=BLUE, size=21)
    s.box(940, 145, 230, 80, "TERMINATED", colors=GREY, size=22)
    s.box(80, 505, 240, 90, "BLOCKED", colors=ORANGE, size=22)
    s.box(445, 505, 240, 90, "WAITING", colors=VIOLET, size=22)
    s.box(800, 505, 340, 90, "TIMED_WAITING", colors=YELLOW, size=22)
    s.arrow([(250, 185), (430, 185)], label="start()", label_offset=(0, -22))
    s.arrow([(750, 185), (940, 185)], label="run() returns or throws", label_offset=(0, -22))
    s.arrow([(500, 230), (200, 505)], color=ORANGE[0], start_arrow=True)
    s.arrow([(590, 230), (565, 505)], color=VIOLET[0], start_arrow=True)
    s.arrow([(680, 230), (970, 505)], color=YELLOW[0], start_arrow=True)
    s.text(250, 365, "enter: monitor unavailable\nreturn: lock acquired", size=17)
    s.text(565, 365, "enter: wait / join / park\nreturn: notify / completion / unpark", size=17)
    s.text(900, 365, "enter: sleep / timed wait, join, or park\nreturn: timeout or signal", size=17)
    s.text(610, 675, "RUNNABLE includes both executing in the JVM and eligible to execute.", size=18)
    return s


def java_memory_sharing() -> Scene:
    s = Scene(
        "java-memory-sharing",
        "Thread stacks and shared heap objects",
        "Each thread has a private stack, but local references can point to the same mutable object in the shared heap.",
        1120,
        650,
        ["book/java/images/threadsafe.jpeg"],
    )
    s.heading("Stack slots are private; referenced objects may be shared")
    s.rect(80, 110, 610, 465, stroke=ORANGE[0], fill="#fff4e6")
    s.text(385, 140, "Heap (shared)", size=23, weight=500)
    s.box(220, 235, 330, 190, "Mutable object\nfields / members\nreachable from static state", colors=ORANGE, size=20)
    s.rect(760, 110, 285, 210, stroke=GREEN[0], fill="#ebfbee")
    s.text(902, 140, "Thread A stack", size=21, weight=500)
    s.box(805, 180, 195, 55, "local primitive", colors=GREEN, size=17)
    s.box(805, 250, 195, 45, "local reference", colors=CYAN, size=17)
    s.rect(760, 365, 285, 210, stroke=GREEN[0], fill="#ebfbee")
    s.text(902, 395, "Thread B stack", size=21, weight=500)
    s.box(805, 435, 195, 55, "local primitive", colors=GREEN, size=17)
    s.box(805, 505, 195, 45, "local reference", colors=CYAN, size=17)
    s.arrow([(805, 272), (550, 300)], color=CYAN[0])
    s.arrow([(805, 527), (650, 527), (650, 380), (550, 380)], color=CYAN[0])
    s.text(385, 530, "Thread safety depends on whether mutable state is shared and coordinated.", size=17)
    return s


def java_classloader_delegation() -> Scene:
    s = Scene(
        "java-classloader-delegation",
        "Java class-loader parent delegation",
        "The application loader delegates to the platform loader, which delegates to bootstrap; if a parent cannot load a class, the request falls back toward the child loader's findClass implementation.",
        1120,
        660,
        ["book/java/images/jvm-classloader.png"],
    )
    s.heading("Parent-first class loading")
    s.box(90, 250, 250, 100, "Application\nclass loader", colors=BLUE, size=21)
    s.box(435, 250, 250, 100, "Platform\nclass loader", colors=GREEN, size=21)
    s.box(780, 250, 250, 100, "Bootstrap\nclass loader", colors=ORANGE, size=21)
    s.arrow([(340, 275), (435, 275)], label="delegate", label_offset=(0, -22))
    s.arrow([(685, 275), (780, 275)], label="delegate", label_offset=(0, -22))
    s.arrow([(780, 330), (685, 330)], label="not found", label_offset=(0, 22), dashed=True)
    s.arrow([(435, 330), (340, 330)], label="not found", label_offset=(0, 22), dashed=True)
    s.box(110, 470, 210, 75, "findClass", colors=VIOLET, size=21)
    s.arrow([(215, 350), (215, 470)], label="define class", label_offset=(95, 0))
    s.ellipse(215, 125, 125, 38, "loadClass(name)", colors=GREY, size=18)
    s.arrow([(215, 163), (215, 250)])
    s.text(560, 600, "Class identity = binary name + defining class loader", size=19, weight=500)
    return s


def spring_service_discovery() -> Scene:
    s = Scene(
        "spring-service-discovery",
        "Service registration and discovery flow",
        "Service instances register with a discovery server; a client looks up the service, receives an instance location, and then calls that instance.",
        1160,
        680,
        [
            "book/spring/images/service-discovery-components.png",
            "book/spring/images/service0discovery-flow.png",
        ],
    )
    s.heading("Registration and lookup are separate paths")
    s.box(430, 110, 300, 110, "Discovery server\nservice registry", colors=BLUE, size=22)
    s.box(100, 440, 260, 110, "Application client", colors=ORANGE, size=22)
    s.box(785, 385, 260, 95, "Service instance A", colors=GREEN, size=20)
    s.box(785, 520, 260, 95, "Service instance B", colors=GREEN, size=20)
    s.arrow([(785, 420), (670, 220)], color=GREEN[0], label="1  register + heartbeat", label_offset=(55, -14))
    s.arrow([(785, 555), (620, 220)], color=GREEN[0])
    s.arrow([(230, 440), (430, 195)], color=ORANGE[0], label="2  lookup service", label_offset=(-75, -10))
    s.arrow([(430, 215), (310, 440)], color=BLUE[0], label="3  return locations", label_offset=(-70, 24))
    s.arrow([(360, 495), (785, 435)], color=ORANGE[0], label="4  call selected instance", label_offset=(0, -18))
    return s


def spring_cloud_system() -> Scene:
    s = Scene(
        "spring-cloud-system",
        "Components of the legacy Spring Cloud Netflix example",
        "Gateway, discovery, configuration, and two application services with registration, startup configuration, and request dependencies.",
        1200,
        720,
        ["book/spring/images/parts-of-system.png"],
    )
    s.heading("Cloud-native system components")
    s.box(70, 275, 230, 105, "Gateway\n(two instances)", colors=VIOLET, size=21)
    s.box(475, 105, 250, 105, "Discovery\n(two instances)", colors=BLUE, size=21)
    s.box(900, 275, 230, 105, "Config\n(two instances)", colors=ORANGE, size=21)
    s.box(330, 500, 230, 105, "Service A\n(two instances)", colors=GREEN, size=21)
    s.box(650, 500, 230, 105, "Service B\n(two instances)", colors=CYAN, size=21)
    s.arrow([(300, 327), (330, 552)], color=VIOLET[0], label="request", label_offset=(-22, -15))
    s.arrow([(560, 552), (650, 552)], color=GREEN[0], label="dependency", label_offset=(0, -20))
    for x in [185, 445, 765]:
        s.arrow([(x, 500 if x != 185 else 275), (600, 210)], color=BLUE[0], label="register" if x == 445 else None)
    for target in [(185, 380), (445, 500), (765, 500)]:
        s.arrow([(900, 327), target], color=ORANGE[0], dashed=True, label="startup config" if target[0] == 765 else None)
    return s


def spring_startup_config() -> Scene:
    s = Scene(
        "spring-cloud-startup-config",
        "Spring Cloud startup configuration phase",
        "Gateway and application services fetch external configuration from the Config Server during startup.",
        1120,
        570,
        ["book/spring/images/system-on-startup-1.png"],
    )
    s.heading("Startup phase 1: fetch external configuration")
    s.box(820, 210, 240, 115, "Config server", colors=ORANGE, size=23)
    components = [(70, "Gateway", VIOLET), (330, "Service A", GREEN), (590, "Service B", CYAN)]
    for x, label, palette in components:
        s.box(x, 360, 210, 100, label, colors=palette, size=21)
        s.arrow([(x + 105, 360), (900, 325)], color=ORANGE[0], label="GET configuration" if label == "Service A" else None)
    s.text(560, 520, "Each component starts with environment-specific settings before serving traffic.", size=18)
    return s


def spring_startup_registration() -> Scene:
    s = Scene(
        "spring-cloud-startup-registration",
        "Spring Cloud service-registration phase",
        "Gateway and service instances register their network locations and health with the discovery server.",
        1120,
        570,
        ["book/spring/images/system-on-startup-2.png"],
    )
    s.heading("Startup phase 2: register discoverable instances")
    s.box(440, 110, 240, 115, "Discovery server", colors=BLUE, size=23)
    components = [(70, "Gateway", VIOLET), (330, "Service A", GREEN), (590, "Service B", CYAN)]
    for x, label, palette in components:
        s.box(x, 370, 210, 100, label, colors=palette, size=21)
        s.arrow([(x + 105, 370), (560, 225)], color=BLUE[0], label="register + heartbeat" if label == "Service A" else None)
    s.text(560, 525, "The registry can return only instances that have registered and remain healthy.", size=18)
    return s


def spring_transaction_proxy() -> Scene:
    s = Scene(
        "spring-transaction-proxy",
        "Direct method call compared with a transaction proxy",
        "Without a proxy the caller invokes the application object directly; with a Spring transaction proxy, an interceptor begins a transaction, invokes the target, then commits or rolls back.",
        1220,
        650,
        ["book/spring/images/without-proxy.png", "book/spring/images/with-proxy.png"],
    )
    s.heading("@Transactional works when the call crosses the proxy")
    s.text(295, 105, "Without proxy", size=23, weight=500)
    s.box(60, 230, 190, 100, "Calling code", colors=GREY, size=21)
    s.box(360, 205, 250, 150, "Application object\n@Transactional method", colors=GREEN, size=20)
    s.arrow([(250, 280), (360, 280)], label="direct call")
    s.text(330, 420, "No transaction advice surrounds the invocation.", size=17)

    s.line([(650, 90), (650, 590)], color=GREY[0], dashed=True)
    s.text(935, 105, "With proxy", size=23, weight=500)
    s.box(700, 230, 170, 100, "Calling code", colors=GREY, size=21)
    s.box(915, 210, 230, 140, "Transaction proxy\ninterceptor", colors=VIOLET, size=20)
    s.box(915, 455, 230, 110, "Application object\nmethod", colors=GREEN, size=20)
    s.arrow([(870, 280), (915, 280)], label="1  call", label_offset=(0, -18))
    s.arrow([(1030, 350), (1030, 455)], label="2  begin + invoke", label_offset=(-120, -18))
    s.arrow([(1145, 510), (1175, 510), (1175, 330), (1145, 330)], label="3  commit / rollback", label_offset=(-100, 28))
    return s


def hystrix_dashboard_reading() -> Scene:
    s = Scene(
        "hystrix-dashboard-reading",
        "How to read a legacy Hystrix Dashboard command tile",
        "Annotated command tile showing request volume, health, error rate, throughput, circuit state, hosts, and latency percentiles.",
        1200,
        720,
        ["book/spring/images/reading-hystrix-dashboard.png"],
    )
    s.heading("Reading a legacy Hystrix Dashboard command tile")
    s.ellipse(535, 300, 205, 165, "", colors=GREEN)
    s.text(535, 180, "getCurrentWeather", size=22, weight=500)
    s.text(470, 235, "1,135", size=28, color=GREEN[0], weight=500)
    s.text(560, 235, "0", size=23, color=BLUE[0])
    s.text(615, 235, "0", size=23, color=RED[0])
    spark = [(390, 340), (430, 340), (450, 285), (480, 385), (525, 382), (550, 315), (580, 350), (620, 350), (650, 325), (680, 325)]
    s.line(spark, color=BLUE[0], stroke_width=3)
    s.text(535, 420, "Hosts 1   Median 1 ms   Mean 1 ms\np90 2 ms   p99 8 ms   p99.5 8 ms", size=16)
    s.box(810, 210, 250, 62, "Error rate 0.0%", colors=RED, size=19)
    s.box(810, 295, 250, 62, "Throughput 49.7 req/s", colors=BLUE, size=18)
    s.box(810, 380, 250, 62, "Circuit CLOSED", colors=GREEN, size=19)
    s.arrow([(330, 235), (420, 235)], label="circle size = request volume", label_offset=(-130, -20))
    s.arrow([(330, 300), (335, 300)], label="fill = command health", label_offset=(-120, 0))
    s.arrow([(810, 242), (740, 242)], label="failed / rejected / timeout", label_offset=(0, -20))
    s.arrow([(810, 326), (700, 326)], label="requests per second", label_offset=(0, 22))
    s.arrow([(535, 465), (535, 570)], label="latency percentiles (rolling window)", label_offset=(170, 0))
    s.text(535, 645, "The exact UI is legacy; the useful reading order is volume → errors → state → latency.", size=17)
    return s


def go_context_tree() -> Scene:
    s = Scene(
        "go-context-tree",
        "Go context cancellation tree",
        "Canceling a parent context propagates cancellation to every descendant, while canceling a child does not affect its parent or siblings.",
        1080,
        620,
    )
    s.heading("Cancellation flows from parent to descendants")
    s.box(410, 95, 260, 75, "request context", colors=BLUE, size=22)
    s.box(165, 265, 260, 85, "database timeout\n2 seconds", colors=GREEN, size=19)
    s.box(655, 265, 260, 85, "downstream timeout\n500 milliseconds", colors=VIOLET, size=19)
    s.box(65, 455, 220, 80, "query goroutine", colors=GREEN, size=18)
    s.box(305, 455, 220, 80, "audit goroutine", colors=CYAN, size=18)
    s.box(655, 455, 260, 80, "HTTP call goroutine", colors=VIOLET, size=18)
    s.arrow([(475, 170), (295, 265)], color=BLUE[0], label="derive")
    s.arrow([(605, 170), (785, 265)], color=BLUE[0], label="derive")
    s.arrow([(250, 350), (175, 455)], color=GREEN[0])
    s.arrow([(340, 350), (415, 455)], color=GREEN[0])
    s.arrow([(785, 350), (785, 455)], color=VIOLET[0])
    s.text(
        540,
        585,
        "Canceling the parent reaches every descendant; child cancellation stops only that subtree.",
        size=18,
        weight=500,
    )
    return s


def raptor_tree() -> Scene:
    s = Scene(
        "raptor-index-and-retrieve",
        "RAPTOR indexing and retrieval tree",
        "Document chunks are embedded, clustered, and summarized recursively; retrieval may search detailed leaves and higher-level summaries while citations resolve to source chunks.",
        1180,
        720,
    )
    s.heading("RAPTOR builds and searches a hierarchy")
    leaves = [(80, "Chunk 1"), (250, "Chunk 2"), (420, "Chunk 3"), (590, "Chunk 4"), (760, "Chunk 5"), (930, "Chunk 6")]
    for x, label in leaves:
        s.box(x, 545, 140, 65, label, colors=GREY, size=17)
    parents = [(165, "Cluster A\nsummary"), (505, "Cluster B\nsummary"), (845, "Cluster C\nsummary")]
    for x, label in parents:
        s.box(x, 345, 190, 85, label, colors=GREEN, size=18)
    s.box(420, 145, 340, 90, "Higher-level summary", colors=BLUE, size=21)
    for leaf_index, (x, _) in enumerate(leaves):
        parent_x = parents[leaf_index // 2][0] + 95
        s.arrow([(x + 70, 545), (parent_x, 430)], color=GREEN[0])
    for x, _ in parents:
        s.arrow([(x + 95, 345), (590, 235)], color=BLUE[0])
    s.ellipse(1040, 155, 95, 38, "query", colors=ORANGE, size=20)
    s.arrow([(945, 155), (760, 190)], color=ORANGE[0], label="search summaries", label_offset=(0, -20))
    s.arrow([(1040, 193), (1040, 545)], color=ORANGE[0], label="search leaves", label_offset=(70, 0), dashed=True)
    s.text(590, 675, "Answer evidence retains lineage back to the original chunks.", size=18, weight=500)
    return s


def opentelemetry_collector_pipeline() -> Scene:
    s = Scene(
        "opentelemetry-collector-pipeline",
        "OpenTelemetry Collector pipeline",
        "Applications send telemetry to receivers, which pass it through ordered processors and then exporters to one or more observability backends.",
        1180,
        590,
    )
    s.heading("A signal pipeline wires receivers → processors → exporters")
    s.box(55, 215, 185, 120, "Applications\nOTLP gRPC / HTTP", colors=GREY, size=19)
    s.box(310, 215, 190, 120, "Receiver\notlp", colors=BLUE, size=20)
    s.box(570, 155, 210, 90, "Processor\nmemory_limiter", colors=YELLOW, size=18)
    s.box(570, 305, 210, 90, "Processor\nbatch", colors=YELLOW, size=19)
    s.box(850, 215, 190, 120, "Exporter\nOTLP / debug", colors=GREEN, size=19)
    s.box(850, 445, 260, 80, "Observability backend", colors=VIOLET, size=19)
    s.arrow([(240, 275), (310, 275)], color=GREY[0])
    s.arrow([(500, 275), (535, 275), (535, 200), (570, 200)], color=BLUE[0])
    s.arrow([(675, 245), (675, 305)], color=YELLOW[0])
    s.arrow([(780, 350), (815, 350), (815, 275), (850, 275)], color=YELLOW[0])
    s.arrow([(945, 335), (945, 445)], color=GREEN[0])
    s.text(590, 555, "Components do nothing until referenced under service.pipelines.<signal>.", size=18, weight=500)
    return s


def data_engineering_pipeline() -> Scene:
    s = Scene(
        "data-engineering-pipeline",
        "Data engineering platform stages",
        "Sources flow through ingestion, durable raw storage, transformation, and serving; observability spans every stage and enables replay, lineage, and freshness checks.",
        1200,
        560,
    )
    s.heading("A dependable data path preserves replay and lineage")
    boxes = [
        (45, "Sources\nDB · API · files · events", GREY),
        (285, "Ingest\nbatch + streaming", BLUE),
        (525, "Store raw\nhistory for replay", CYAN),
        (765, "Transform\nvalidated models", GREEN),
        (1005, "Serve\nBI · ML · apps", VIOLET),
    ]
    for index, (x, label, palette) in enumerate(boxes):
        s.box(x, 185, 170, 110, label, colors=palette, size=18)
        if index:
            s.arrow([(boxes[index - 1][0] + 170, 240), (x, 240)])
    s.rect(225, 375, 790, 90, stroke=ORANGE[0], fill=ORANGE[1], dashed=True)
    s.text(620, 405, "Observe every stage", size=21, weight=500)
    s.text(620, 440, "freshness · volume · schema · quality · lineage · cost · failures", size=17)
    for x, _, _ in boxes[1:]:
        s.arrow([(x + 85, 295), (x + 85, 375)], color=ORANGE[0], dashed=True)
    s.arrow([(850, 465), (610, 520), (370, 465)], color=RED[0], label="replay / backfill", label_offset=(0, 20))
    return s


def main() -> None:
    scenes = [
        kubernetes_nodeport_single(),
        kubernetes_nodeport_cluster(),
        kubernetes_clusterip(),
        java_heap_layout(),
        java_generational_heap(),
        java_contiguous_vs_g1(),
        java_thread_states(),
        java_memory_sharing(),
        java_classloader_delegation(),
        spring_service_discovery(),
        spring_cloud_system(),
        spring_startup_config(),
        spring_startup_registration(),
        spring_transaction_proxy(),
        hystrix_dashboard_reading(),
        go_context_tree(),
        raptor_tree(),
        opentelemetry_collector_pipeline(),
        data_engineering_pipeline(),
    ]
    for scene in scenes:
        scene.write()
    print(f"Generated {len(scenes)} Excalidraw scenes and SVG exports in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
