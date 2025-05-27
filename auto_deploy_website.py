import os
import shutil
import subprocess

def run_cmd(cmd, cwd=None):
    print(f"👉 执行命令: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd)
    if result.returncode != 0:
        print("❌ 命令执行失败！")
        exit(1)

def main():
    # 1. 删除 website 目录
    website_dir = os.path.join(os.getcwd(), "website")
    if os.path.exists(website_dir):
        print("🧹 正在删除 website 目录...")
        shutil.rmtree(website_dir)

    # 2. git clone docs 分支到 website 目录
    repo_url = "git@github.com:pysunday/pysunday.github.io.git"
    print("📥 正在克隆 docs 分支到 website...")
    run_cmd(f"git clone {repo_url} website")

    # 3. 复制 site/ 下所有文件到 website/
    site_dir = os.path.join(os.getcwd(), "site")
    if not os.path.exists(site_dir):
        print("❌ 错误: site 目录不存在！")
        exit(1)

    print("📋 正在复制 site 内容到 website...")
    for item in os.listdir(site_dir):
        s = os.path.join(site_dir, item)
        d = os.path.join(website_dir, item)
        if os.path.isdir(s):
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)

    # 4. 在 website 目录执行 git push
    print("🚀 准备 push 到远程仓库...")
    run_cmd("git add .", cwd=website_dir)
    run_cmd('git commit -m "自动更新 website 内容"', cwd=website_dir)
    run_cmd("git push", cwd=website_dir)

    print("✅ 全部完成！")

if __name__ == "__main__":
    main()

