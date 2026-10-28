"""Exercise profile installation without fetching unpublished GitHub assets."""

import os
from pathlib import Path
import re
import subprocess
import tempfile
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "skills/rust-magic-linter/assets"
PROFILES = ("minimal", "standard", "maximum")
DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ParkSnoopy/rust-magic-linter/main/"
PACKAGE = '''[package]
name = "profile-fixture"
version = "0.1.0"
edition = "2024"
description = "Fixture for installed Rust lint profiles"
license = "MIT"
repository = "https://github.com/ParkSnoopy/rust-magic-linter"
readme = "README.md"
keywords = ["lint"]
categories = ["development-tools"]
'''
CLEAN_SOURCE = (
    '//! Profile installation fixture.\n'
    'fn main() { let _ = std::env::var_os("PROFILE_FIXTURE"); }\n'
)
# Intercept only the transport boundary; execute the actual installer in Bash.
DOWNLOAD_FIXTURE = r'''
curl() {
    [[ $1 = -fsSL ]] || return 90
    shift
    local relative=${1#"$TEST_DOWNLOAD_ROOT"}
    [[ $relative != "$1" && $relative != *..* ]] || return 91
    printf '%s\n' "$relative" >> "$TEST_REQUESTS"
    [[ -z $TEST_FAIL_DOWNLOAD || $relative != *"$TEST_FAIL_DOWNLOAD" ]] || return 22
    if [[ ${2:-} = -o ]]; then
        cp "$TEST_ROOT/$relative" "$3"
    else
        printf '%s\n' "$(< "$TEST_ROOT/$relative")"
    fi
}
export -f curl
if [[ $TEST_INLINE = yes ]]; then
    bash -c "$(< "$TEST_INSTALLER")" -- "$@"
else
    bash "$TEST_INSTALLER" "$@"
fi
'''


class InstallTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(
            prefix="rust-magic-linter-", dir=os.environ.get("TMPDIR")
        )
        self.addCleanup(directory.cleanup)
        self.directory = Path(directory.name)

    def project(self, name="project", workspace=False):
        project = self.directory / name
        project.mkdir()
        package = project / "member" if workspace else project
        package.mkdir(exist_ok=True)
        (package / "src").mkdir()
        (package / "src/main.rs").write_text(CLEAN_SOURCE)
        (package / "README.md").write_text("# Profile fixture\n")
        (package / "Cargo.toml").write_text(PACKAGE)
        if workspace:
            (project / "Cargo.toml").write_text(
                '[workspace]\nmembers = ["member"]\nresolver = "3"\n'
            )
        return project, package

    def install(self, project, preset=None, answers="y\ny\n", fail="", inline=False):
        environment = os.environ | {
            "TEST_ROOT": str(ROOT),
            "TEST_INSTALLER": str(ROOT / "scripts/install.sh"),
            "TEST_DOWNLOAD_ROOT": DOWNLOAD_ROOT,
            "TEST_REQUESTS": str(project / "requests.log"),
            "TEST_FAIL_DOWNLOAD": fail,
            "TEST_INLINE": "yes" if inline else "no",
        }
        arguments = [] if preset is None else [preset]
        return subprocess.run(
            ["bash", "-c", DOWNLOAD_FIXTURE, "fixture", *arguments],
            cwd=project, env=environment, input=answers, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=30,
        )

    def clippy(self, project):
        return subprocess.run(
            ["cargo", "clippy", "--offline", "--workspace", "--all-targets"],
            cwd=project, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, timeout=120,
        )

    def test_all_profile_bundles_install_and_enforce_lints(self):
        for profile in PROFILES:
            for workspace in (False, True):
                with self.subTest(profile=profile, workspace=workspace):
                    project, package = self.project(f"{profile}-{workspace}", workspace)
                    result = self.install(project, profile)
                    self.assertEqual(result.returncode, 0, result.stdout)
                    manifest = tomllib.loads((project / "Cargo.toml").read_text())
                    actual = manifest["workspace"] if workspace else manifest
                    expected = tomllib.loads((ASSETS / profile / "lint.toml").read_text())
                    self.assertEqual(actual["lints"], expected["lints"])
                    for name in ("clippy.toml", "CONSTITUTION.md"):
                        self.assertEqual(
                            (project / name).read_bytes(),
                            (ASSETS / profile / name).read_bytes(),
                        )
                    self.assertEqual(
                        (project / ".cargo/deny.toml").read_bytes(),
                        (ASSETS / "deny.toml").read_bytes(),
                    )
                    requests = (project / "requests.log").read_text().splitlines()
                    self.assertEqual(requests, [
                        f"skills/rust-magic-linter/assets/{profile}/lint.toml",
                        f"skills/rust-magic-linter/assets/{profile}/clippy.toml",
                        "skills/rust-magic-linter/assets/deny.toml",
                        f"skills/rust-magic-linter/assets/{profile}/CONSTITUTION.md",
                    ])
                    if workspace:
                        with (package / "Cargo.toml").open("a") as manifest_file:
                            manifest_file.write("\n[lints]\nworkspace = true\n")
                    result = self.clippy(project)
                    self.assertEqual(result.returncode, 0, result.stdout)
                    (package / "src/main.rs").write_text(
                        '//! Rejected unwrap fixture.\n'
                        'fn main() { let _ = std::env::var("PROFILE_FIXTURE").unwrap(); }\n'
                    )
                    result = self.clippy(project)
                    self.assertNotEqual(result.returncode, 0, result.stdout)
                    self.assertRegex(result.stdout, r"clippy::unwrap[-_]used")

    def test_inline_invocation_selects_each_profile(self):
        for profile in PROFILES:
            with self.subTest(profile=profile):
                project, _ = self.project(profile)
                result = self.install(project, profile, answers="n\ny\n", inline=True)
                self.assertEqual(result.returncode, 0, result.stdout)
                self.assertEqual(
                    (project / "CONSTITUTION.md").read_bytes(),
                    (ASSETS / profile / "CONSTITUTION.md").read_bytes(),
                )
                self.assertFalse((project / ".cargo").exists())

    def test_default_profile_declines_optional_files_at_eof(self):
        project, _ = self.project()
        result = self.install(project, answers="")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("Using preset: standard", result.stdout)
        self.assertFalse((project / "CONSTITUTION.md").exists())
        self.assertFalse((project / ".cargo").exists())

    def test_existing_companion_files_are_preserved(self):
        for name in ("clippy.toml", ".clippy.toml"):
            with self.subTest(name=name):
                project, _ = self.project(name)
                (project / name).write_text("# Existing Clippy configuration\n")
                (project / "CONSTITUTION.md").write_text("# Existing constitution\n")
                result = self.install(project, "maximum", answers="n\ny\n")
                self.assertEqual(result.returncode, 0, result.stdout)
                self.assertEqual((project / name).read_text(), "# Existing Clippy configuration\n")
                self.assertEqual((project / "CONSTITUTION.md").read_text(), "# Existing constitution\n")
                self.assertNotIn("/clippy.toml", (project / "requests.log").read_text())
                if name == ".clippy.toml":
                    self.assertFalse((project / "clippy.toml").exists())

    def test_existing_lints_and_invalid_profiles_do_not_modify_manifest(self):
        for profile in (*PROFILES, "invalid"):
            for workspace in (False, True):
                with self.subTest(profile=profile, workspace=workspace):
                    project, _ = self.project(f"{profile}-{workspace}", workspace)
                    manifest = project / "Cargo.toml"
                    if profile != "invalid":
                        table = "workspace.lints.clippy" if workspace else "lints.clippy"
                        with manifest.open("a") as output:
                            output.write(f'\n[{table}]\nunwrap_used = "warn"\n')
                    before = manifest.read_bytes()
                    result = self.install(project, profile)
                    self.assertNotEqual(result.returncode, 0, result.stdout)
                    self.assertEqual(manifest.read_bytes(), before)
                    self.assertFalse((project / "requests.log").exists())

    def test_required_download_failures_leave_manifest_unchanged(self):
        for name in ("lint.toml", "clippy.toml"):
            with self.subTest(name=name):
                project, _ = self.project(name)
                before = (project / "Cargo.toml").read_bytes()
                result = self.install(project, "standard", fail=name)
                self.assertEqual(result.returncode, 22, result.stdout)
                self.assertEqual((project / "Cargo.toml").read_bytes(), before)
                self.assertFalse((project / "clippy.toml").exists())
                self.assertNotIn("Installation complete", result.stdout)

    def test_parent_lint_tables_are_not_duplicated(self):
        for table in ("lints", "workspace.lints", " workspace . lints . clippy "):
            with self.subTest(table=table):
                project, _ = self.project(table)
                manifest = project / "Cargo.toml"
                with manifest.open("a") as output:
                    output.write(f"\n[{table}]\n")
                before = manifest.read_bytes()
                result = self.install(project, "standard")
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertEqual(manifest.read_bytes(), before)
                self.assertFalse((project / "requests.log").exists())

    def test_root_package_workspace_can_inherit_profile_lints(self):
        project, _ = self.project()
        manifest = project / "Cargo.toml"
        with manifest.open("a") as output:
            output.write('\n[ workspace ]\nmembers = []\nresolver = "3"\n')
        result = self.install(project, "maximum", answers="")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("The root package also needs", result.stdout)
        with manifest.open("a") as output:
            output.write("\n[lints]\nworkspace = true\n")
        result = self.clippy(project)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_bundles_share_baseline_and_consistent_comments(self):
        minimal = (ASSETS / "minimal/CONSTITUTION.md").read_text()
        standard = (ASSETS / "standard/CONSTITUTION.md").read_text()
        maximum = (ASSETS / "maximum/CONSTITUTION.md").read_text()
        self.assertTrue(standard.startswith(minimal))
        self.assertTrue(maximum.startswith(standard))
        comments = {}
        for profile in PROFILES:
            self.assertEqual(
                {path.name for path in (ASSETS / profile).iterdir()},
                {"lint.toml", "clippy.toml", "CONSTITUTION.md"},
            )
            self.assertEqual(
                (ASSETS / profile / "clippy.toml").read_bytes(),
                (ASSETS / "minimal/clippy.toml").read_bytes(),
            )
            for line in (ASSETS / profile / "lint.toml").read_text().splitlines():
                match = re.match(r'(\w+)\s*=\s*"\w+"\s+# (.+)', line)
                if match:
                    key, comment = match.groups()
                    self.assertEqual(comments.setdefault(key, comment), comment, key)


if __name__ == "__main__":
    unittest.main()
