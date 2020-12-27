from aws_cdk import (
    core,
    aws_kms as kms,
    aws_cloudtrail as cloudtrail,
    aws_iam as iam,
)


class TrailStack(core.Stack):

    def __init__(self, scope: core.Construct,
                 construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # CloudTrailの暗号化キーを作成
        trail_key = kms.Key(
            self, 'TrailKey',
            alias='TrailKey',
            enable_key_rotation=True
        )

        # 証跡を作成
        cloudtrail.Trail(
            self, 'trail',
            trail_name='trail',
            encryption_key=trail_key,
            send_to_cloud_watch_logs=True
        )

        # CloudTrailに暗号化権限を付与するポリシーを定義
        key_policy = iam.PolicyStatement()
        key_policy.add_service_principal("cloudtrail.amazonaws.com")
        key_policy.add_actions("kms:GenerateDataKey*")
        key_policy.add_all_resources()
        key_policy.add_condition('StringLike', {
            'kms:EncryptionContext:aws:cloudtrail:arn':
            'arn:aws:cloudtrail:*:' + self.account + ':trail/*'
        })

        # 暗号化キーにポリシーを付与
        trail_key.add_to_resource_policy(key_policy)
