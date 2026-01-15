
#
#   'navigation': Returns HTML + CSS Specific to the sliding navigation between pages.
#

def getNavigation():
    return f"""

    <style>
        {getCSS()}
    </style>
    {getHTML()}

    """

def getCSS():
    return """

    :root {
    --color-neutral-100: oklch(0.141 0.005 285.823);
    --color-neutral-200: oklch(0.21 0.006 285.885);
    --color-accent: white;
    --color-accent-hover: #dedede;
    --color-text: black;
    --rounding: .5rem;
    --sidebar-toggler-size: 3rem;
    }

    @property --sidebar-width {
    syntax: "<number>";
    initial-value: 0;
    inherits: true;
    }
    @keyframes openSidebar {
    from {
        --sidebar-width: 0 ;
    }
    to {
        --sidebar-width: 16;
    }
    }
    @keyframes closeSidebar {
    from {
        --sidebar-width: 16;
    }
    to {
        --sidebar-width: 0 ;
    }
    }
    body {
    color: var(--color-text);
    background: var(--color-neutral-100);
    }

    .wrapper {
    background: var(--color-neutral-100);
    container-type: inline-size;
    }
    .wrapper:has(#sidebar-toggler-input:checked) {
    animation: 0.25s ease openSidebar;
    --sidebar-width: 16;
    }
    .wrapper:not(:has(#sidebar-toggler-input:checked)) {
    animation: 0.25s ease closeSidebar;
    --sidebar-width: 0;
    }

    .sidebar {
    z-index: 9999;
    background-color: var(--color-accent);
    position: absolute;
    right: -16rem;
    left: auto;
    top: 0;
    bottom: 0;
    display: flex;
    align-items: stretch;
    justify-content: stretch;
    width: 16rem;
    transform: translateX(calc(var(--sidebar-width) * -1rem));
    }

    .sidebar-content {
    position: relative;
    height: 100%;
    width: 100%;
    }

    .mobile-slide-nav {
    list-style: none;
    padding-top: 0.22rem;
    color: black;
    }

    .mobile-slide-nav li {
    color: black;
    text-decoration: none;
    }

    .sidebar-toggler {
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: center;
    left: calc(var(--sidebar-toggler-size) * -1);
    right: auto;
    top: 0;
    background: var(--color-accent);
    height: var(--sidebar-toggler-size);
    width: var(--sidebar-toggler-size);
    border: 0;
    border-bottom-left-radius: var(--rounding);
    cursor: pointer;
    transition: 0.15s ease;
    z-index: 50;
    }


    .sidebar-toggler-icon {
    fill: var(--color-text);
    height: calc(var(--sidebar-toggler-size) * 0.5);
    width: calc(var(--sidebar-toggler-size) * 0.5);
    }
    .sidebar-toggler:hover {
    background: var(--color-accent-hover);
    }
    .sidebar-toggler input {
    display: none;
    }

    .content {
    position: relative;
    background: var(--color-neutral-200);
    padding: 3rem 2rem 1rem;
    }
    .content > * {
    max-width: 48rem;
    }

    .padding {
    padding: 1rem;
    }

    a {
    color: var(--color-accent);
    text-decoration: none;
    transition: 0.2s ease color;
    }
    a:hover {
    color: var(--color-accent-hover);
    }/*# sourceMappingURL=style.css.map */

    """

def getHTML():
    return """

    <aside class="sidebar">
        <div class="sidebar-content">
            <label class="sidebar-toggler">
                <svg viewBox="0 0 448 512" width="100" title="bars" class="sidebar-toggler-icon">
                    <path d="M16 132h416c8.837 0 16-7.163 16-16V76c0-8.837-7.163-16-16-16H16C7.163 60 0 67.163 0 76v40c0 8.837 7.163 16 16 16zm0 160h416c8.837 0 16-7.163 16-16v-40c0-8.837-7.163-16-16-16H16c-8.837 0-16 7.163-16 16v40c0 8.837 7.163 16 16 16zm0 160h416c8.837 0 16-7.163 16-16v-40c0-8.837-7.163-16-16-16H16c-8.837 0-16 7.163-16 16v40c0 8.837 7.163 16 16 16z" />
                </svg>
                <input id="sidebar-toggler-input" type="checkbox" />
            </label>
            <div class="padding">
                <ul class="mobile-slide-nav">
                    <li><a href='#education-divider'>Education</a></li>
                    <li><a href='#projects-divider'>Projects</a></li>
                    <li><a href='#experience-divider'>Experience</a></li>
                    <li><a href='#tech-divider'>Full Tech Stack</a></li>
                </ul>
            </div>
        </div>
    </aside>

    """