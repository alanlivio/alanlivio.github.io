import os
import sys
import json
import urllib.request
import urllib.error
import yaml

def fetch_repo_stats(repo_name):
    url = f"https://api.github.com/repos/{repo_name}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "zensical-builder-macros"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            return {
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0)
            }
    except Exception as e:
        print(f"Warning: Failed to fetch stats for {repo_name} in macro: {e}", file=sys.stderr)
        return None

def define_env(env):
    script_path = os.path.abspath(__file__)
    current_mtime = os.path.getmtime(script_path)
    base_dir = os.path.dirname(script_path)
    cache_path = os.path.join(base_dir, ".github_stats_cache.json")
    md_path = os.path.join(base_dir, "docs", "opensource.md")

    # Initialize stats dict and totals
    stats = {}
    total_stars = 0
    total_forks = 0
    total_repos = 0

    cache_valid = False
    cache_data = None
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
                if cache_data.get("macros_mtime") == current_mtime:
                    cache_valid = True
                    stats = cache_data.get("stats", {})
                    total_stars = cache_data.get("total_stars", 0)
                    total_forks = cache_data.get("total_forks", 0)
                    total_repos = cache_data.get("total_repos", 0)
        except Exception:
            pass

    if not cache_valid:
        print("Zensical Macros: macros.py edited or cache missing. Fetching fresh GitHub stats...")
        repos = []
        if os.path.exists(md_path):
            try:
                with open(md_path, "r", encoding="utf-8") as f:
                    content = f.read()
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    metadata = yaml.safe_load(parts[1])
                    for section in metadata.get("sections", []):
                        for repo in section.get("repositories", []):
                            if repo.get("name"):
                                repos.append(repo["name"])
            except Exception as e:
                print(f"Error parsing opensource.md: {e}", file=sys.stderr)

        total_repos = len(repos)
        success = True
        new_stats = {}
        for name in repos:
            repo_stats = fetch_repo_stats(name)
            if repo_stats is not None:
                new_stats[name] = repo_stats
                total_stars += repo_stats["stars"]
                total_forks += repo_stats["forks"]
            else:
                success = False
                old_repo_stats = stats.get(name, {"stars": 0, "forks": 0})
                new_stats[name] = old_repo_stats
                total_stars += old_repo_stats["stars"]
                total_forks += old_repo_stats["forks"]

        stats = new_stats

        try:
            cache_payload = {
                "total_repos": total_repos,
                "total_stars": total_stars,
                "total_forks": total_forks,
                "stats": stats
            }
            if success:
                cache_payload["macros_mtime"] = current_mtime
                print("Zensical Macros: GitHub repository stats successfully updated and cached.")
            else:
                if cache_data and "macros_mtime" in cache_data:
                    cache_payload["macros_mtime"] = cache_data["macros_mtime"]
                print("Zensical Macros: Some fetches failed. Stats cached but cache mtime not updated to allow retry.")
            
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(cache_payload, f)
        except Exception as e:
            print(f"Error writing cache: {e}", file=sys.stderr)

    env.variables["github_total_repos"] = total_repos
    env.variables["github_total_stars"] = total_stars
    env.variables["github_total_forks"] = total_forks
    env.variables["github_stats"] = stats

    page = None
    import inspect
    frame = inspect.currentframe()
    while frame:
        if "page" in frame.f_locals:
            page = frame.f_locals["page"]
            if page:
                break
        frame = frame.f_back

    if page and page.meta.get("template") == "opensource.html":
        page.meta["total_repos"] = total_repos
        page.meta["total_stars"] = total_stars
        page.meta["total_forks"] = total_forks

        for section in page.meta.get("sections", []):
            for repo in section.get("repositories", []):
                name = repo.get("name")
                if name and name in stats:
                    repo["stars"] = stats[name]["stars"]
                    repo["forks"] = stats[name]["forks"]

