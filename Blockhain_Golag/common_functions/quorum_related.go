package common_functions

type ValidatorData struct {
	ValidatorPubKey string
	TotalStake      *big.Int
}

func GetFromApprovementThreadState(poolId string) *structures.PoolStorage {
	if val, ok := globals.APPROVEMENT_THREAD_METADATA_HANDLER.Handler.Cache[poolId]; ok {
		return val
	}

	data, err := globals.APPROVEMENT_THREAD_METADATA.Get([]byte(poolId), nil)
	if err != nil {
		return nil
	}

	var pool structures.PoolStorage
	err = json.Unmarshal(data, &pool)
	if err != nil {
		return nil
	}

	globals.APPROVEMENT_THREAD_METADATA_HANDLER.Handler.Cache[poolId] = &pool
	return &pool
}

func SetLeadersSequence(epochHandler *structures.EpochDataHandler, epochSeed string) {
	epochHandler.LeadersSequence = []string{}

	hashOfMetadataFromOldEpoch := utils.Blake3(epochSeed)
	validatorsExtendedData := make(map[string]ValidatorData)
	totalStakeSum := big.NewInt(0)

	for validatorPubKey := range epochHandler.PoolsRegistry {
		validatorData := GetFromApprovementThreadState(validatorPubKey + "(POOL)_STORAGE_POOL")
		totalStakeByThisValidator := new(big.Int).Add(new(big.Int), validatorData.TotalStaked.Int)
		totalStakeSum.Add(totalStakeSum, totalStakeByThisValidator)
		validatorsExtendedData[validatorPubKey] = ValidatorData{validatorPubKey, totalStakeByThisValidator}
	}

	for i := range len(epochHandler.PoolsRegistry) {
		cumulativeSum := big.NewInt(0)
		hashInput := hashOfMetadataFromOldEpoch + "_" + strconv.Itoa(i)
		deterministicRandomValue := new(big.Int)
		deterministicRandomValue.SetString(utils.Blake3(hashInput), 16)
		deterministicRandomValue.Mod(deterministicRandomValue, totalStakeSum)

		for validatorPubKey, validator := range validatorsExtendedData {
			cumulativeSum.Add(cumulativeSum, validator.TotalStake)
			if deterministicRandomValue.Cmp(cumulativeSum) <= 0 {
				epochHandler.LeadersSequence = append(epochHandler.LeadersSequence, validatorPubKey)
				totalStakeSum.Sub(totalStakeSum, validator.TotalStake)
				delete(validatorsExtendedData, validatorPubKey)
				break
			}
		}
	}
}

func GetQuorumMajority(epochHandler *structures.EpochDataHandler) int {
	quorumSize := len(epochHandler.Quorum)
	majority := (2 * quorumSize) / 3
	majority += 1
	if majority > quorumSize {
		return quorumSize
	}
	return majority
}

func GetQuorumUrlsAndPubkeys(epochHandler *structures.EpochDataHandler) []structures.QuorumMemberData {
	var toReturn []structures.QuorumMemberData
	for _, pubKey := range epochHandler.Quorum {
		poolStorage := GetFromApprovementThreadState(pubKey + "(POOL)_STORAGE_POOL")
		toReturn = append(toReturn, structures.QuorumMemberData{PubKey: pubKey, Url: poolStorage.PoolUrl})
	}
	return toReturn
}

func GetCurrentEpochQuorum(epochHandler *structures.EpochDataHandler, quorumSize int, newEpochSeed string) []string {
	totalNumberOfValidators := len(epochHandler.PoolsRegistry)

	if totalNumberOfValidators <= quorumSize {
		futureQuorum := make([]string, 0, len(epochHandler.PoolsRegistry))
		for validatorPubkey := range epochHandler.PoolsRegistry {
			futureQuorum = append(futureQuorum, validatorPubkey)
		}
		return futureQuorum
	}

	quorum := []string{}
	hashOfMetadataFromEpoch := utils.Blake3(newEpochSeed)
	validatorsExtendedData := make(map[string]ValidatorData)
	totalStakeSum := big.NewInt(0)

	for validatorPubKey := range epochHandler.PoolsRegistry {
		validatorData := GetFromApprovementThreadState(validatorPubKey + "(POOL)_STORAGE_POOL")
		totalStakeByThisValidator := new(big.Int).Add(new(big.Int), validatorData.TotalStaked.Int)
		validatorsExtendedData[validatorPubKey] = ValidatorData{
			ValidatorPubKey: validatorPubKey,
			TotalStake:      totalStakeByThisValidator,
		}
		totalStakeSum.Add(totalStakeSum, totalStakeByThisValidator)
	}

	for i := range quorumSize {
		cumulativeSum := big.NewInt(0)
		hashInput := hashOfMetadataFromEpoch + "_" + strconv.Itoa(i)
		deterministicRandomValue := new(big.Int)
		deterministicRandomValue.SetString(utils.Blake3(hashInput), 16)
		deterministicRandomValue.Mod(deterministicRandomValue, totalStakeSum)

		for validatorPubKey, validator := range validatorsExtendedData {
			cumulativeSum.Add(cumulativeSum, validator.TotalStake)
			if deterministicRandomValue.Cmp(cumulativeSum) <= 0 {
				quorum = append(quorum, validatorPubKey)
				totalStakeSum.Sub(totalStakeSum, validator.TotalStake)
				delete(validatorsExtendedData, validatorPubKey)
				break
			}
		}
	}

	return quorum
}
