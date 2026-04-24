from infrawatch.deployment.domain.models.rollout_status import RolloutStatus


class TestRolloutStatus:
    def test_rollout_is_ready(self) -> None:
        status = RolloutStatus(ready=True, replicas=3, available=3)

        assert status.is_ready() is True

    def test_rollout_not_ready(self) -> None:
        status = RolloutStatus(ready=False, replicas=3, available=1)

        assert status.is_ready() is False

    def test_rollout_all_replicas_available(self) -> None:
        status = RolloutStatus(ready=True, replicas=3, available=3)

        assert status.all_available() is True

    def test_rollout_not_all_replicas_available(self) -> None:
        status = RolloutStatus(ready=True, replicas=3, available=2)

        assert status.all_available() is False
