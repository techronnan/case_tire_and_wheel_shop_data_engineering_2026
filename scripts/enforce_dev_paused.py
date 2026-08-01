"""Garante que o Job [dev] fique pausado, mesmo que alguem despause manualmente
pela UI. Usa DATABRICKS_HOST/DATABRICKS_TOKEN do ambiente (mesmo padrao do CLI)."""
import dataclasses

from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import PauseStatus

TARGET_NAME = "[dev] wf_pneustore_carrinho_abandonado"


def main():
    w = WorkspaceClient()
    for job in w.jobs.list():
        settings = job.settings
        if not settings or settings.name != TARGET_NAME:
            continue
        sched = settings.schedule
        if sched and sched.pause_status == PauseStatus.UNPAUSED:
            print(f"ATIVO -> pausando: {settings.name} (id={job.job_id})")
            new_sched = dataclasses.replace(sched, pause_status=PauseStatus.PAUSED)
            new_settings = dataclasses.replace(settings, schedule=new_sched)
            w.jobs.update(job_id=job.job_id, new_settings=new_settings)
        else:
            print(f"OK: {settings.name}")
        return
    print(f"Job '{TARGET_NAME}' nao encontrado ainda (normal no primeiro deploy)")


if __name__ == "__main__":
    main()
