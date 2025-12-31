#!/usr/bin/env python3
"""
Docker Environment Verification Script
Checks Docker, API keys, dependencies, and connectivity before launching
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

class DockerVerifier:
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.success = []
        self.project_root = Path(__file__).parent

    def check_docker_installed(self) -> bool:
        """Check if Docker is installed"""
        try:
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                self.success.append(f"✓ Docker installed: {version}")
                return True
            else:
                self.issues.append("✗ Docker installed but failed to run")
                return False
        except FileNotFoundError:
            self.issues.append(
                "✗ Docker not found. Install from: https://www.docker.com/products/docker-desktop"
            )
            return False
        except Exception as e:
            self.issues.append(f"✗ Docker check failed: {e}")
            return False

    def check_docker_daemon(self) -> bool:
        """Check if Docker daemon is running"""
        try:
            result = subprocess.run(
                ["docker", "ps"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                self.success.append("✓ Docker daemon is running")
                return True
            else:
                self.issues.append("✗ Docker daemon is not running. Start Docker Desktop.")
                return False
        except Exception as e:
            self.issues.append(f"✗ Docker daemon check failed: {e}")
            return False

    def check_docker_compose(self) -> bool:
        """Check if Docker Compose is installed"""
        try:
            result = subprocess.run(
                ["docker-compose", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                self.success.append(f"✓ Docker Compose installed: {version}")
                return True
            else:
                self.issues.append("✗ Docker Compose not found or failed")
                return False
        except FileNotFoundError:
            self.issues.append(
                "✗ Docker Compose not found. Install: docker-compose or Docker Desktop"
            )
            return False
        except Exception as e:
            self.issues.append(f"✗ Docker Compose check failed: {e}")
            return False

    def check_configuration_files(self) -> bool:
        """Check if required Docker config files exist"""
        required_files = [
            "Dockerfile",
            "docker-compose.yml",
            "requirements-docker.txt",
            ".dockerignore",
            "entrypoint.sh"
        ]
        
        all_exist = True
        for filename in required_files:
            filepath = self.project_root / filename
            if filepath.exists():
                self.success.append(f"✓ {filename} exists")
            else:
                self.issues.append(f"✗ {filename} missing")
                all_exist = False
        
        return all_exist

    def check_env_file(self) -> bool:
        """Check if docker.env is configured"""
        env_file = self.project_root / "docker.env"
        example_file = self.project_root / "docker.env.example"
        
        if not env_file.exists():
            if example_file.exists():
                self.warnings.append(
                    "⚠ docker.env not found. Copy from docker.env.example and add your OpenAI API key"
                )
                return False
            else:
                self.issues.append("✗ docker.env.example not found")
                return False
        
        # Check if API key is set
        try:
            with open(env_file) as f:
                content = f.read()
                if "OPENAI_API_KEY=" in content or "OPENAI_API_KEY=" in content:
                    # Simple check - actual validation happens at runtime
                    if content.count("OPENAI_API_KEY=") > 0:
                        self.success.append("✓ docker.env found with API key configured")
                        return True
                    else:
                        self.warnings.append(
                            "⚠ docker.env exists but OPENAI_API_KEY may not be set correctly"
                        )
                        return False
                else:
                    self.warnings.append(
                        "⚠ OPENAI_API_KEY not properly configured in docker.env"
                    )
                    return False
        except Exception as e:
            self.issues.append(f"✗ Error reading docker.env: {e}")
            return False

    def check_docker_resources(self) -> bool:
        """Check Docker resource allocation"""
        try:
            result = subprocess.run(
                ["docker", "system", "df"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                self.success.append("✓ Docker can access system resources")
                return True
            else:
                self.warnings.append("⚠ Could not verify Docker resource access")
                return False
        except Exception as e:
            self.warnings.append(f"⚠ Docker resource check failed: {e}")
            return False

    def check_port_availability(self, port: int = 8501) -> bool:
        """Check if required port is available"""
        try:
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                result = sock.connect_ex(('127.0.0.1', port))
                if result != 0:
                    self.success.append(f"✓ Port {port} is available")
                    return True
                else:
                    self.warnings.append(
                        f"⚠ Port {port} is already in use. Change in docker-compose.yml if needed"
                    )
                    return False
        except Exception as e:
            self.warnings.append(f"⚠ Port availability check failed: {e}")
            return False

    def check_disk_space(self) -> bool:
        """Check if sufficient disk space available"""
        try:
            import shutil
            stat = shutil.disk_usage(self.project_root)
            free_gb = stat.free / (1024**3)
            
            if free_gb > 5:
                self.success.append(f"✓ Sufficient disk space: {free_gb:.1f}GB free")
                return True
            else:
                self.warnings.append(f"⚠ Low disk space: {free_gb:.1f}GB free (5GB+ recommended)")
                return False
        except Exception as e:
            self.warnings.append(f"⚠ Disk space check failed: {e}")
            return False

    def check_application_files(self) -> bool:
        """Check if RAG application files exist"""
        required_dirs = ["core", "utils", "config"]
        required_files = ["app.py"]
        
        all_exist = True
        
        for directory in required_dirs:
            dirpath = self.project_root / directory
            if dirpath.is_dir():
                self.success.append(f"✓ {directory}/ directory exists")
            else:
                self.issues.append(f"✗ {directory}/ directory missing")
                all_exist = False
        
        for filename in required_files:
            filepath = self.project_root / filename
            if filepath.exists():
                self.success.append(f"✓ {filename} exists")
            else:
                self.issues.append(f"✗ {filename} missing")
                all_exist = False
        
        return all_exist

    def print_report(self):
        """Print verification report"""
        print("\n" + "="*60)
        print("  RAG Application - Docker Verification Report")
        print("="*60 + "\n")
        
        # Success messages
        if self.success:
            print("✓ PASSED CHECKS:")
            for msg in self.success:
                print(f"  {msg}")
            print()
        
        # Warning messages
        if self.warnings:
            print("⚠ WARNINGS:")
            for msg in self.warnings:
                print(f"  {msg}")
            print()
        
        # Issues
        if self.issues:
            print("✗ ISSUES TO FIX:")
            for msg in self.issues:
                print(f"  {msg}")
            print()
            return False
        else:
            print("✓ All checks passed! You're ready to launch Docker.\n")
            print("NEXT STEPS:")
            print("  1. Run: docker-compose up --build")
            print("  2. Access: http://localhost:8501")
            print("  3. Upload documents and start asking questions!")
            print()
            return True

    def run_all_checks(self) -> bool:
        """Run all verification checks"""
        print("\nRunning Docker verification checks...\n")
        
        checks = [
            ("Docker Installation", self.check_docker_installed),
            ("Docker Daemon", self.check_docker_daemon),
            ("Docker Compose", self.check_docker_compose),
            ("Configuration Files", self.check_configuration_files),
            ("Environment File", self.check_env_file),
            ("Docker Resources", self.check_docker_resources),
            ("Port Availability", self.check_port_availability),
            ("Disk Space", self.check_disk_space),
            ("Application Files", self.check_application_files),
        ]
        
        results = []
        for check_name, check_func in checks:
            try:
                result = check_func()
                results.append((check_name, result))
            except Exception as e:
                self.issues.append(f"✗ {check_name} check crashed: {e}")
                results.append((check_name, False))
        
        return self.print_report()


def main():
    """Main entry point"""
    verifier = DockerVerifier()
    
    try:
        success = verifier.run_all_checks()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nVerification cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nFatal error during verification: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
