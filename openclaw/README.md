# OpenClaw 项目配置汇总

## 生成时间
- UTC: 2026-03-28T11:16:08.626Z

## Agents
- main [default] -> /root/.openclaw/agents/main/agent
- writer -> /root/.openclaw/agents/writer
- IT -> /root/.openclaw/agents/IT
- person -> /root/.openclaw/agents/person
- finance -> /root/.openclaw/agents/finance
- design -> /root/.openclaw/agents/design
- marketing -> /root/.openclaw/agents/marketing
- sales -> /root/.openclaw/agents/sales
- product -> /root/.openclaw/agents/product
- mentor -> /root/.openclaw/agents/mentor
- tech -> /root/.openclaw/agents/tech
- info -> /root/.openclaw/agents/info

## Bindings
- main <= {"channel":"feishu","accountId":"default"}
- writer <= {"channel":"feishu","accountId":"bot-1774678552517"}
- it <= {"channel":"feishu","accountId":"it"}
- person <= {"channel":"feishu","accountId":"person"}
- finance <= {"channel":"feishu","accountId":"finance"}
- design <= {"channel":"feishu","accountId":"design"}
- marketing <= {"channel":"feishu","accountId":"marketing"}
- sales <= {"channel":"feishu","accountId":"sales"}
- product <= {"channel":"feishu","accountId":"product"}
- mentor <= {"channel":"feishu","accountId":"mentor"}
- tech <= {"channel":"feishu","accountId":"tech"}
- info <= {"channel":"feishu","accountId":"info"}

## Feishu Accounts
- bot-1774678552517: 鲁迅 (enabled)
- it: 比尔·盖茨 (enabled)
- default: OpenClaw助手 (enabled)
- person: 柳比歇夫 (enabled)
- finance: 巴菲特 (enabled)
- design: 宋徽宗 (enabled)
- marketing: 奥格威 (enabled)
- sales: 罗永浩 (enabled)
- product: 乔布斯 (enabled)
- mentor: 王阳明 (enabled)
- tech: 凯文·凯利 (enabled)
- info: 福尔摩斯 (enabled)

## 安全提示
- config/raw-* 含敏感密钥（App Secret / API Key），请勿直接外发
- config/sanitized/openclaw.sanitized.json 可用于共享或提交仓库
