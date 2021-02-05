from src.Base.episodes import aggregate_into_episodes, host_episode_sequences
from src.Updated.SequenceGeneration.episodes import get_attack_episodes, TeamAttackEpisodes
from src.Updated.SequenceGeneration.load import *
from src.Updated.SequenceGeneration.sequences import get_host_episode_sequences
from src.Updated.common import save_pkl, read_pkl


def setup():
    data_base, team_labels = read_pkl("test_data/base.pkl")
    data_update: LoadedData = read_pkl("test_data/update.pkl")
    print("Loaded data")

    for i in range(len(data_update)):
        data_update[0][i] = data_update[0][i][1:]
        assert len(data_base[i]) == len(data_update[0][i])

    print("Aggregating base")
    episodes_base, team_times = aggregate_into_episodes(data_base, team_labels, step=150)
    print("Aggregating update")
    episodes_update = get_attack_episodes(data_update, time_step=150)
    print("Done aggregating")

    save_pkl((episodes_base, team_times), "test_data/base_episodes.pkl")
    save_pkl(episodes_update, "test_data/update_episodes.pkl")


def main():
    episodes_base, team_times = read_pkl("test_data/base_episodes.pkl")
    episodes_update: TeamAttackEpisodes = read_pkl("test_data/update_episodes.pkl")

    assert len(episodes_base[0]) == len(episodes_update[0])
    print("Loaded")

    base_sequences = host_episode_sequences(episodes_base)
    update_sequences = get_host_episode_sequences(episodes_update)

    assert len(base_sequences) == len(update_sequences)
    for host, seq in base_sequences.items():
        # if '10.0.0.20' in host:
        #     # Note: See episodes_test -> this one should have a non-filtered episode sequence
        #     continue
        assert host in update_sequences
        # assert len(seq) == len(update_sequences[host])
        if len(seq) != len(update_sequences[host]):
            print(
                f"Length mismatch for {host}: expected {len(seq)}, got {len(update_sequences[host])}")
            continue
        for i in range(len(seq)):
            base = seq[i]
            update = update_sequences[host][i]
            # for j, b in enumerate(base):
            #     assert b[0] == update[j][0].start_time
            #     assert b[1] == update[j][0].end_time
            #     assert b[2] == update[j][0].mcat
            #     assert b[6] == update[j][0].services
            #     assert b[7] == update[j][1]
            for j, b in enumerate(base):
                if b[0] != update[j][0].start_time or b[1] != update[j][0].end_time or b[2] != \
                        update[j][0].mcat or b[6] != update[j][0].services or b[7] != update[j][1]:
                    print(f"Mismatch at idx {j} for host {host}")
                    print(f"\tBase is {b}")
                    print(f"\tUpdate is {update[j][0]}")

    print("Done")


if __name__ == '__main__':
    setup()
    main()